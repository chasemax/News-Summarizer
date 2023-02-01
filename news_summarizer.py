import feedparser
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

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

# This is a list of the RSS feeds we are subscribing to for security news
newsSources = {
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews?format=xml',
    'Graham Cluley': 'https://www.grahamcluley.com/feed/',
    'Krebs on Security': 'http://krebsonsecurity.com/feed/',
    'Threatpost': 'https://threatpost.com/feed/',
    'Naked Security': 'https://nakedsecurity.sophos.com/feed/'
}

articleTexts = []

for title, source in newsSources.items():
    # For every news source, we get the RSS feed. 
    feed = feedparser.parse(source)

    for article in feed['items']:
        #For every article in the feed, we open the web page
        html = urllib.request.urlopen(article['link']).read()

        #Then we extract the text from the web page and put it in an object
        articleTexts.append({
            "title" : article['title'],
            "body" : text_from_html(html)
        })
        break # Remove to loop through all sources; currently we just get one article from each source


# This secion outputs all of the articles in a nice format
print("""
  _____     __             _  __             
 / ___/_ __/ /  ___ ____  / |/ /__ _    _____
/ /__/ // / _ \/ -_) __/ /    / -_) |/|/ (_-<
\___/\_, /_.__/\__/_/   /_/|_/\__/|__,__/___/
    /___/  


The Latest in Cybersecurity News!
""")
for article in articleTexts:
    print("---------------------------------")
    print(article['title'])
    print("---")
    print(article['body'])