import feedparser

# Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 
    
# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines( rss_url ):
    headlines = []
    
    feed = parseRSS( rss_url )
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    
    return headlines

# A list to hold all headlines
allheadlines = []

# List of RSS feeds that we will fetch and combine
newsurls = {
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews?format=xml',
    'Graham Cluley': 'https://www.grahamcluley.com/feed/',
    'Schneier on Security': 'https://www.schneier.com/blog/atom.xml',
}

# Iterate over the feed urls
for key,url in newsurls.items():
    # Call getHeadlines() and combine the returned headlines with allheadlines
    allheadlines.extend( getHeadlines( url ) )


# Iterate over the allheadlines list and print each headline
for hl in allheadlines:
    print(hl)