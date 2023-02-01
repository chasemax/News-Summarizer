# IS 565 January Creation Project
## Team 3
*Michael Bramwell, Nathan Gardner, Chase Maxfield, Nathan Moser, Devin Rockwood*

## Project

For our project, we are creating a linux tool that gather security articles from around the interent using RSS Feeds and web scraping, it will then compile all the articles in a nice repository for easy viewing from security professionals.

Initially we are planning on it being commandline based for ease of initial development, but will introduce a GUI/web app later on.

In addition, we hope to use a text summarizer tool and natural language processing to slim down the amount of news for busy cybersecurity professionals. 

## Using this tool

Run the following command:
```
python news_summarizer.py
```

## How it works so far

The tool first queries several of the top RSS feeds for cybersecurity news using the feedparser library. It then extracts the links from each of the articles it has received in the feed and fetches the actual web pages containing those articles. From each of those articles, it extracts the readable body text by identifying the p tags on those web pages. Finally, it compiles all of those articles into one output for the reader.

## Usefulness of this tool

> "Staying on top of cybersecurity news also helps CISOs and security managers ensure their teams are well-informed and aware of emerging threats. Knowing what’s happening in the cyber industry today helps your team prepare for tomorrow."
- Cybersn.com

> "With a 1,070 percent increase in ransomware attacks year-over-year between July 2020 and June 2021, staying on top of attack trends—such as ransomware and supply chain threats—is more important than ever. To successfully detect and defend against security threats, we need to come together as a community and share our expertise, research, intelligence, and insights."
- Microsoft

Cybersecurity professionals need to stay curent with cybersecurity news because new exploits and vulnerabilities are developed all the time. They run the risk of not discovering vulnerabilities in their own systems and major threats if they are not aware of the threat landscape that faces them. This tool will help cybersecurity professionals stay up to date with these threats while minimizing the amount of time that they'll need to research the threats. 

## References
Tools used:
- https://jcutrer.com/python/python-tutorial-howto-parse-rss-headlines
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
