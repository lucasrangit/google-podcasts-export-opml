# Export Google Podcasts Subscriptions

Unlike most podcasting apps, Google Podcasts does not support an export (or import) feature. This repository contains tools you can use to export your Google Podcasts subscriptions as OPML.

It performs the following steps.

1. Scrape for podcasts
1. Lookups RSS feeds
1. Save as OPML

## Podcast Index API

A free https://podcastindex.org/ API key is required to perform the podcast title to RSS feed lookup.

1. Sign up at https://api.podcastindex.org/signup
1. Save API key and secret receive via email to 'secrets.txt'. For example:
```
podcastindex_config = {
    "api_key": "KEY",
    "api_secret": "SECRET"
}
```

## Usage

1. On the https://podcasts.google.com/subscriptions, run the contents of 'scape.js' in your web browser's console.
1. Copy the resulting object and save it to a new file named 'data.json'.
1. Run `python3 scrape.py`.
1. Review the results in 'podcasts.opml'.
