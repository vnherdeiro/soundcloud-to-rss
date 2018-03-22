#! /usr/bin/python3

from sys import argv, exit
import re
import urllib
from bs4 import BeautifulSoup as bs
from time import time


BASE_URL = "https://soundcloud.com/"
RSS_FORMAT = "http://feeds.soundcloud.com/users/soundcloud:users:{}/sounds.rss"
COPY_TO_CLIPBOARD = True

class WebpageScraper:
	"""
	Object reading web pages from URL and outputting them as a BeautifulSoup soup object
	"""
	def __init__(self, delay_between_queries=0):
		self.opener = urllib.request.build_opener()
		self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		self.lastQuery = -float("inf")
		self.delay_between_queries = delay_between_queries
	def readUrl( self, url_):
		waiting_time = -(time() - self.lastQuery - self.delay_between_queries)
		if waiting_time > 0:
			sleep( waitingTime)
		webpage_handle = self.opener.open(url_)
		webpage_content = webpage_handle.read()
		self.lastQuery = time()
		return bs(webpage_content, "html.parser")
	def __call__( self, url_):
		return self.readUrl( url_)

class ResultItem:
	def __init__(self, text, url):
		self.text = text
		self.url = url
	def __repr__(self):
		return "<search result for %s>" %self.text

class SearchSoundCloud:
	def __init__(self, search_arguments=[], scraper=WebpageScraper()):
		self.scraper = scraper
		if search_arguments: #search arguments passed as cmd line arguments
			search_query = " ".join( search_arguments)
		else: #search arguments passed by user kb input
			print("Which soundcloud feed are you looking for?")
			search_query = input()
		search_url = self.SearchUrl( search_query)
		self.search_soup = scraper( search_url)
		self.feed_url = None

	def SearchPageToFeed(self):
		"""
		Parses the soundcloud search result page, offers choices to user and translates choice to feed url
		"""
		try:
			research_results = self.search_soup.find_all("ul")[1].find_all("a")
			results = {index: ResultItem(x.text, x["href"][1:]) for index, x in enumerate(research_results,start=1)}
		except IndexError:
			print( "Search gave no results..")
			exit()
		else:
			print()
			for result_index, result in results.items():
				print( "%2d:  %s" %(result_index, result.text))
			user_input_index = None
			print("\nWhich one is it? (enter index)")
			while not user_input_index in results:
				try:
					user_input_index = int( input())
				except ValueError:
					user_input_index = None
			self.feed_url = BASE_URL + results[user_input_index].url

	def FeedToUrl(self):
		"""
		Reads the RSS url from SoundCloud feed mainpage
		"""
		sc_user_soup = self.scraper( self.feed_url)
		try:
			sc_userid = next(re.finditer("users:(\d+)", str(sc_user_soup))).group(1)
		except StopIteration:
			print( "Problem reading Soundcloud user ID")
		else:
			rss_url = RSS_FORMAT.format(sc_userid)
			print()
			print( "-"*100)
			print( "{:^100}".format(rss_url))
			print( "-"*100)
			if COPY_TO_CLIPBOARD:
				try:
					import pyperclip
					pyperclip.copy( rss_url)
				except:
					pass

	@staticmethod
	def SearchUrl( search_items):
		"""
		Returns the soundcloud search url from search inputs
		"""
		return BASE_URL + "search/people?q=" + urllib.parse.quote_plus(search_items)

if __name__ == "__main__":
	search_arguments = argv[1:]
	scraper = WebpageScraper()
	feed_search = SearchSoundCloud(search_arguments, scraper)
	feed_search.SearchPageToFeed()
	feed_search.FeedToUrl()
