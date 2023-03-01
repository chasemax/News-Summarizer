# IS 565 February Creation Project
## Team 3
*Michael Bramwell, Nathan Gardner, Chase Maxfield, Nathan Moser, Devin Rockwood*

## Project

For our project, we are creating a linux tool that gather security articles from around the interent using RSS Feeds and web scraping. After gathering these security articles, it then uses topic analysis and text summary tools from hugging face to slim down the amount of news for busy cybersecurity professionals.

## Installation

You will need the following python libraries in order to use this tool:
- spacy
- transformers (from hugging face)
- feedparser
- beautifulsoup4

When this script runs for the first time, it will need to download a summarization model from hugging face, which it will do automatically. It will take ~1GiB of space.

## Using this tool

This tool often requires several minutes to run to completion depending on your hardware, due to the heavy amount of machine learning it uses. Run the following command and let it run to completion:
```
python news_summarizer.py
```

Also included in the repo are two iterations of .ipynb we used to piecewise assemble the summarizers, including a first attempt. They are not necessary to run the tool; they simply exist to show some of the development process.

## How it works so far

The tool first queries several of the top RSS feeds for cybersecurity news using the feedparser library. It then extracts the links from each of the articles it has received in the feed and fetches the actual web pages containing those articles. From each of those articles, it extracts the readable body text by identifying the p tags on those web pages. 

The tool then extracts all of the proper nouns from each article that occur at least once and likely several times. It then compares each news source's top proper nouns to see which proper nouns appear across the most news sources, hopefully identifying the most important news topics of the day. It then summarizes all of the news article that contain those proper nouns by first performing extractive summarization, which identifies the top sentences in each

## Actual news summaries from the tool

Date: 2/28/2023

Topic: Ukraine 

Russia's cyber attacks against Ukraine surged by 250% in 2022 when compared to two years ago, Google's Threat Analysis Group and Mandiant disclosed in a new joint report . Russia’s military intelligence service, the GRU, “launched destructive wiper attacks on hundreds of systems in Ukrainian government, IT, energy, and financial organizations,” Microsoft said . Despite Russia's conventional military setbacks and its failure to substantively advance its agenda through cyber operations, Russia maintains its intent to bring Ukraine under Russian control .

Topic: Windows 

January brings 10 critical updates as well as 67 patches rated as important to the Windows platform . With Windows 10 21H2 now out of mainstream support, we have the following Microsoft applications that will reach end of support or servicing in 2023 . With all of these more difficult testing scenarios, we recommend that you scan your application portfolio for updated application components or system-level dependencies . Given the large number of changes included this month, I have broken down the testing scenarios into high risk and standard risk groups .

Obviously, these summaries are not perfect, but given a larger transformer model, the outputs could probably improve significantly. Future versions of this tool could use the GPT-3 API to summarize the articles.

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
- https://www.activestate.com/blog/how-to-do-text-summarization-with-python/
- https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
