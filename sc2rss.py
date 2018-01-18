#! /usr/bin/python3

from sys import argv, exit
import re
import urllib
from bs4 import BeautifulSoup as bs
from time import time


BASE_URL = "https://soundcloud.com/"
RSS_FORMAT = "http://feeds.soundcloud.com/users/soundcloud:users:{}/sounds.rss"
COPY_TO_CLIPBOARD = True

class PageScrapper():
	def __init__(self, delay_between_queries=0):
		self.opener = urllib.request.build_opener()
		self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		self.lastQuery = -float("inf")
		self.delay_between_queries = delay_between_queries
	def readUrl( self, url_):
		presentTime = time() - self.lastQuery - self.delay_between_queries
		if presentTime < 0:
			sleep( abs(presentTime))
		inData = self.opener.open(url_)
		content = inData.read()
		self.lastQuery = time()
		return bs(content, "html.parser")
	def __call__( self, url_):
		return self.readUrl( url_)

def SearchUrl( search_items):
	"""
	Returns the soundcloud search url from search inputs
	"""
	return BASE_URL + "search/people?q=" + urllib.parse.quote_plus(search_items)

class ResultItem:
	def __init__(self, text, url):
		self.text = text
		self.url = url
	def __repr__(self):
		return "<search result for %s>" %self.text
	

if len(argv) > 1:
	search_items = " ".join( argv[1:])
else:
	print("What soundcloud feed are you looking for?")
	search_items = input()
search_url = SearchUrl( search_items)
scrapper = PageScrapper()



search_soup = scrapper( search_url)
try:
	research_results = search_soup.find_all("ul")[1].find_all("a")
	results = {index: ResultItem(x.text, x["href"][1:]) for index, x in enumerate(research_results,start=1)}
except IndexError:
	print( "Search gave no results..")
	exit()
else:
	print()
	for result_index, result in results.items():
		print( "%2d:  %s" %(result_index, result.text))
	user_index = None
	print("\nWhich one is it? (enter index)")
	while not user_index in results:
		user_index = int( input())
	sc_user_url = BASE_URL + results[user_index].url

#To get the RSS url, we only need to read some user id number from the user page source
sc_user_soup = scrapper( sc_user_url)
try:
	sc_userid = next(re.finditer("users:(\d+)", str(sc_user_soup))).group(1)
except StopIteration:
	print( "Problem reading Soundcloud user ID")
	exit()
else:
	rss_url = RSS_FORMAT.format(sc_userid)
	print( "\n\t%s" % rss_url)
	if COPY_TO_CLIPBOARD:
		try:
			import pyperclip
			pyperclip.copy( rss_url)
		except:
			pass
