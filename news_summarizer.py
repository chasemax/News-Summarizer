import feedparser
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.find_all('p', text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.get_text() for t in visible_texts)

newsSources = {
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews?format=xml',
    'Graham Cluley': 'https://www.grahamcluley.com/feed/',
    'Krebs on Security': 'http://krebsonsecurity.com/feed/',
    'Threatpost': 'https://threatpost.com/feed/',
    'Naked Security': 'https://nakedsecurity.sophos.com/feed/'
}

articleTexts = []

for title, source in newsSources.items():
    feed = feedparser.parse(source)
    for article in feed['items']:
        html = urllib.request.urlopen(article['link']).read()
        articleTexts.append({
            "title" : article['title'],
            "body" : text_from_html(html)
        })
        break # Remove to loop through all sources; currently we just get one article from each source

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

"""
Steps:
1. Get a bunch of article summaries (from 5 news sites).
2. See if you can start adding parsing for each individual feed. 
"""