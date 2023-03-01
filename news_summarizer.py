
############################### IMPORTS ###############################


# These imports and modifications are necessary for the two summarizer functions

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

from transformers import pipeline

updated_punctuation = punctuation + "”"

# These imports are necessary for the HTML parser to work
import feedparser
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request


############################## FUNCTIONS ###############################


# This function takes in a collection of articles from each news source
# And calculates the top nouns for each article in that news source

def top_proper_nouns_per_article(collection, nlp, prop_noun_threshold=0.1):
    collection_noun_choices = []

    # Loop over all the articles in the news source
    for doc in collection:

        # We extract all the proper nouns from the article using spacy's library
        processed_doc = nlp(doc)
        all_prop_nouns = [token.lemma_ for token in processed_doc if token.pos_ == "PROPN"]
        prop_noun_count = len(all_prop_nouns)
        
        # Next, we count up how many times each proper noun appeared in the article
        noun_counts = dict()

        for noun in all_prop_nouns:
            if noun in noun_counts:
                noun_counts[noun] += 1
            else:
                noun_counts[noun] = 1

        # Finally, we filter out the nouns that appeared less than a minimum threshold
        final_noun_choices = [k for k,v in noun_counts.items() if (v / prop_noun_count) > prop_noun_threshold]

        collection_noun_choices.append(final_noun_choices)

    # We return the list of documents along with the nouns we selected for each document
    return list(zip(collection, collection_noun_choices))

# This function was mostly copied from https://www.activestate.com/blog/how-to-do-text-summarization-with-python/
# It extracts the sentences from a text that contain the most important keywords in that text
def extraction_summarize(text, target_length, nlp):
    doc = nlp(text)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in updated_punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    sentence_tuples = [(sentence, score) for sentence, score in sentence_scores.items()]
    sentence_tuples.sort(key = lambda x: x[1], reverse=True)
    summary = ""

    sentence_number = 0

    while (len(summary.split()) < target_length and sentence_number < len(sentence_tuples)):
        summary += sentence_tuples[sentence_number][0].text
        sentence_number += 1
        
    return summary

# This function performs abstraction summarization on a given text, using neural networks to 
# write a whole new summary for the given text.
def abstraction_summarize(original_text):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary_text = summarizer(original_text, min_length = 100)
    return summary_text[0]['summary_text']

# This function returns whether or not a particular tag is visible to the viewer of a web page
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# This function extracts the readable content text from a webpage
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.find_all('p', text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.get_text() for t in visible_texts)

# This function defines a progress bar that we can use to show how far along we are in the process
# It was taken from https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


############################## MAIN PROGRAM #################################

print("""
  _____     __             _  __             
 / ___/_ __/ /  ___ ____  / |/ /__ _    _____
/ /__/ // / _ \/ -_) __/ /    / -_) |/|/ (_-<
\___/\_, /_.__/\__/_/   /_/|_/\__/|__,__/___/
    /___/  


The Latest in Cybersecurity News!
""")

# This is a list of the RSS feeds we are subscribing to for security news
newsSources = {
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews?format=xml',
    #'Graham Cluley': 'https://www.grahamcluley.com/feed/',
    'Krebs on Security': 'http://krebsonsecurity.com/feed/',
    'Threatpost': 'https://threatpost.com/feed/',
    'Naked Security': 'https://nakedsecurity.sophos.com/feed/',
    'Davinci Forensics': 'https://davinciforensics.co.za/cybersecurity/feed/',
    'Tech Republic': 'https://www.techrepublic.com/rssfeeds/topic/security/?feedType=rssfeeds',
    'Computer World': 'https://www.computerworld.com/uk/category/security/index.rss'
}

source_articles = dict()

for title, source in newsSources.items():

    articleTexts = []

    # For every news source, we get the RSS feed. 
    feed = feedparser.parse(source)

    # Progress bar for each news source
    l = len(feed['items'])
    printProgressBar(0, l, prefix = 'Getting news source: ' + title, suffix = 'Complete', length = 50)

    for i, article in enumerate(feed['items']):

        #For every article in the feed, we open the web page
        html = urllib.request.urlopen(article['link']).read()

        #Then we extract the text from the web page and put it in an object
        articleTexts.append(text_from_html(html))

        printProgressBar(i + 1, l, prefix = 'Getting news source: ' + title, suffix = 'Complete', length = 50)

    source_articles[source] = articleTexts


# Load the natural language processing library beforehand so we don't have to load it each time we make a call to it
nlp = spacy.load('en_core_web_sm')

all_sources_proper_noun_counts = dict()

# Progress bar for proper noun extraction
l = len(source_articles)
i = 0
printProgressBar(0, l, prefix = 'Extracting Proper Nouns', suffix = 'Complete', length = 50)

# For every source, we extract the proper nouns from its articles and add their counts to a dictionary
for source, articles in source_articles.items():

    i += 1
    printProgressBar(i, l, prefix = 'Extracting Proper Nouns', suffix = 'Complete', length = 50)
    source_proper_noun_counts = top_proper_nouns_per_article(articles, nlp=nlp)

    all_sources_proper_noun_counts[source] = source_proper_noun_counts

# Here we calculate the top proper nouns across all the different news sources
all_proper_nouns = {}

for source, articles in all_sources_proper_noun_counts.items():
    for article_text, noun_choices in articles:
        for noun in noun_choices:
            if noun in all_proper_nouns:
                all_proper_nouns[noun] += 1
            else:
                all_proper_nouns[noun] = 1

sorted_proper_nouns = sorted(all_proper_nouns.items(), key=lambda x: x[1], reverse=True)

# We should only take articles that appear in multiple news sources
top_article_nouns = [noun for noun, count in all_proper_nouns.items() if count > 1]
top_article_nouns = top_article_nouns[:10]
print("Topics to summarize are: ", top_article_nouns)

# Now let's get all the articles that contain each top proper noun
top_articles = dict()
all_articles = []
for articles in all_sources_proper_noun_counts.values():
    all_articles.extend(articles)
for noun in top_article_nouns:
    top_articles[noun] = [article_text for article_text, noun_choices in all_articles if noun in noun_choices]

all_summaries = {}

# Progress bar for topic summarization
l = 10
i = 0
printProgressBar(0, l, prefix = 'Summarizing News', suffix = 'Complete', length = 50)

# Finally, we summarize all the articles that belong to a particular topic
for topic, articles in top_articles.items():
    full_text = ""
    for article in articles:
        full_text += article + " "
    
    i += 1
    printProgressBar(i, l, prefix = 'Summarizing News', suffix = 'Complete', length = 50)
    all_summaries[topic] = abstraction_summarize(extraction_summarize(full_text, 500, nlp))

# This section outputs all of the summaries in a nice format

for topic, summary in all_summaries.items():
    print("\n---------------\n")
    print("Topic:", topic, "\n")
    print(summary)