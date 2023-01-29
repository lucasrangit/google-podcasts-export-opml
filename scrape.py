#!/usr/bin/env python3
import re
import urllib.parse
import xml.sax.saxutils as saxutils
from pprint import pprint
from secrets import \
    podcastindex_config  # create file with https://podcastindex.org API key
from sys import exit

import podcastindex
import requests
from bs4 import BeautifulSoup

# TODO add requests-cache https://requests-cache.readthedocs.io/en/stable/

def get_google_podcast_url_from_file(filename):
    podcasts = {}

    with open(filename, "r") as file:
        soup = BeautifulSoup(file, 'html.parser')

        html = soup.find("scrolling-carousel").find("span")
        # print(html.prettify())

        for a in soup.find_all('a'):
            img = a.find('img')
            if img:
                name = img.get("alt")
                if name == "":
                    continue
                url = a.get("href")
                if url == "":
                    continue
                podcasts[name] = url

    return podcasts

def extract_podcast_rss_feed_from_podcastaddict(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        link_tags = soup.find_all("link", type="application/rss+xml")
        if len(link_tags) >= 2:
            return link_tags[1]["href"]
        else:
            return None
    else:
        print(f"Failed to fetch URL: {url}")

def podcasts_get_rss_feed(podcasts):
    rss_feeds = {}

    getrss_url = "https://getrssfeed.com/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    for name, url in podcasts.items():
        # urlencoded = urllib.parse.quote(url, safe="")
        data = {}
        data["url"] = url

        response = requests.post(getrss_url, headers=headers, data=data)

        # Check the status code of the response
        if response.status_code != 200:
            print("Request failed with status code:", response.status_code)
            continue

        # print(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')

        div = soup.find("div", {"id": "centertext"})

        # print(div.prettify())

        script = div.find("script")

        # print(script.prettify())

        match = re.search(r'window\.location\.replace\("(.*)"\)', script.text)
        if not match:
            print("URL not found")
            continue

        podcast_url = match.group(1)

        podcast_rss_url = extract_podcast_rss_feed_from_podcastaddict(podcast_url)
        if podcast_rss_url:
            rss_feeds[name] = podcast_rss_url
        else:
            print("No RSS url found")

        # TODO validate that URL contains XML RSS feed

    return rss_feeds

def podcasts_index_get_rss_feed(podcasts):
    rss_feeds = {}

    index = podcastindex.init(podcastindex_config)

    for name, url in podcasts.items():
        print(name)
        try:
            result = index.search(name)
            # pprint(result)
            rss_url = result["feeds"][0]['url']
            rss_feeds[name] = rss_url
        except Exception() as e:
            print(e)

    return rss_feeds

def create_opml_file(data, filename):
    opml = """\
<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head>
    <title>Podcasts</title>
  </head>
  <body>
    <outline text="Podcasts">
"""
    for title, url in data.items():
        escaped_title = saxutils.escape(title, entities={ "'" : "&apos;" })
        opml += f"      <outline type='rss' text='{escaped_title}' xmlUrl='{url}' />\n"

    opml += """    </outline>
  </body>
</opml>"""

    with open(filename, "w") as f:
        f.write(opml)

if __name__ == "__main__":

    # get google podcast dictionary {title, url}
    podcasts = get_google_podcast_url_from_file("Google Podcasts - Subscriptions.html")

    print(f"Extracted {len(podcasts)} podcasts")

    # convert google podcast urls to rss feed urls
    # rss_feeds = podcasts_get_rss_feed(podcasts)

    rss_feeds = podcasts_index_get_rss_feed(podcasts)

    print(f"Found {len(rss_feeds)} RSS feeds")

    pprint(rss_feeds)

    create_opml_file(rss_feeds, "podcasts.opml")

