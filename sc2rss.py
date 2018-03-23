#! /usr/bin/python3

from sys import argv
from soundcloud_search import SearchSoundCloud

if __name__ == "__main__":
	search_arguments = argv[1:]
	feed_search = SearchSoundCloud(search_arguments)
	feed_search.SearchPageToFeed()
	feed_search.FeedToUrl()
