#!/usr/bin/env python3
import json
import xml.sax.saxutils as saxutils
import podcastindex

def podcasts_index_get_rss_feed(podcasts):
    rss_feeds = {}

    index = podcastindex.init(podcastindex_config)

    for name, url in podcasts.items():
        try:
            result = index.search(name)
            rss_url = result["feeds"][0]['url']
            rss_feeds[name] = rss_url
        except Exception as e:
            print(f"Error while searching for {name}: {e}")

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

    opml += """\
    </outline>
  </body>
</opml>"""

    with open(filename, "w") as f:
        f.write(opml)

def get_google_podcast_url_from_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    try:
        podcastindex_config = open("secrets.txt", "r").read().strip()
    except FileNotFoundError as e:
        print("secrets.txt with the PodcastIndex API key is missing.")
        exit(1)

    # get google podcast dictionary from file {title, url}
    podcasts = get_google_podcast_url_from_file('data.json')

    # convert google podcast urls to rss feed urls
    rss_feeds = podcasts_index_get_rss_feed(podcasts)

    # save the podcasts as OPML XML file
    create_opml_file(rss_feeds, "podcasts.opml")

    # summary
    print(f"Found {len(podcasts)} podcasts in data.json")
    print(f"Wrote {len(rss_feeds)} RSS feeds to podcasts.opml")
