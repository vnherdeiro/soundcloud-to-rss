from webscraper import WebpageScraper
from sys import argv, exit
import re
import urllib

BASE_URL = "https://soundcloud.com/"
RSS_FORMAT = "http://feeds.soundcloud.com/users/soundcloud:users:{}/sounds.rss"
COPY_TO_CLIPBOARD = True


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
			return rss_url

	@staticmethod
	def SearchUrl( search_items):
		"""
		Returns the soundcloud search url from search inputs
		"""
		return BASE_URL + "search/people?q=" + urllib.parse.quote_plus(search_items)
