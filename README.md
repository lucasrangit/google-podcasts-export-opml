# Export Google Podcasts Subscriptions

Google Podcasts has an OPML export feature as documented in [Migrating your Podcast Shows from Google Podcasts](https://blog.youtube/news-and-events/migrating-your-podcasts/). But in case that doesn't work, this repository contains client-side JavaScript you can use to export your Google Podcasts subscriptions as OPML.

It performs the following steps.

1. Scrape https://podcasts.google.com/subscriptions for podcasts.
1. Search for RSS feeds using https://api.podcastindex.org/ .
1. Outputs OPML.

P.S. ChatGPT was used to implement this solution (see https://sharegpt.com/c/r8XNKlj).

## Podcast Index API

A free https://podcastindex.org/ API key is required to perform the podcast title to RSS feed lookup.

1. Sign up at https://api.podcastindex.org/signup .
1. Save the API key and secret received via email (or make a new one) in the `apiKey` and `apiSecret` variables in `scrape.js`.

## Usage

1. Go to https://podcasts.google.com/subscriptions .
1. Open your web browser's console.
1. Paste the contents of `scrape.js` and press Enter.
1. Save the output OPML to `podcasts.opml`.
