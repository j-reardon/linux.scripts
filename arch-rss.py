#!/usr/bin/python

import feedparser

d = feedparser.parse('https://www.archlinux.org/feeds/news/')

print(d['feed']['title'] + "\n")
for i in range(3):
    entry = d.entries[i]
    published = entry.published
    print(published + " -- " + entry.title)
    print(entry.description)
    print("\n")
