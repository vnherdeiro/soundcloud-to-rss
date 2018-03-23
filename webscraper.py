from bs4 import BeautifulSoup as bs
from time import time
import urllib

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
