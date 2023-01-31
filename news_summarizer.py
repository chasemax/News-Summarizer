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
    texts = soup.findAll('p', text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.get_text() for t in visible_texts)

newsSources = {
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews?format=xml',
    'Graham Cluley': 'https://www.grahamcluley.com/feed/',
}

articleLinkList = []
articleTexts = []

for title, source in newsSources.items():
    feed = feedparser.parse(source)
    for article in feed['items']:
        articleLinkList.append(article['link'])
        article['summary']
        break

for articleLink in articleLinkList:
    html = urllib.request.urlopen(articleLink).read()
    articleTexts.append(text_from_html(html))

print("CYBERSECURITY NEWS!")
for article in articleTexts:
    print("---------------------------------")
    print(article)