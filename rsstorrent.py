#!/usr/bin/python3
# -*- coding: utf-8 -*-

import feedparser

url = "https://kickass.so/usearch/rar%20x264%20HDTV%20720p%20vikings/?rss=1"

feed = feedparser.parse(url)

#Pour chaque entrée du flux rss
for entry in feed.entries:
  for link in entry.links:
    if link.type == "application/x-bittorrent":
      #On récupère les info qui nous serons utiles.
      url = link.href
      title = entry.title
      filename = entry.torrent_filename
      torrent_hash = entry.torrent_infohash

