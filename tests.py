#! /usr/bin/python3

import unittest
from unittest.mock import patch
from io import StringIO
from soundcloud_search import SearchSoundCloud

def FakeScrapper_gen():
	with open("tests_input/search_content.dat","rb") as f:
		yield f.read()
	with open("tests_input/feed_content.dat","rb") as f:
		yield f.read()
web_content_generator = FakeScrapper_gen()
def FakeScrapper(*args, **kwargs):
	return next(web_content_generator)

class Test_sc2rss(unittest.TestCase):
	"""
	Tests for sc2rss:
		- integration test to check if the program is still able to parse the SoundCloud result page and extract the RSS url information
		- unit test with data from scrapper mocked and fed from files
	"""

	#unit test
	@patch("builtins.input", return_value="1")
	@patch( "http.client.HTTPResponse.read", side_effect=FakeScrapper)
	def test_mock_scrapper(self, *args, **kwargs):
		search_arguments = ["studio404", "paris"]
		with patch('sys.stdout', new=StringIO()) as silence_stdout:
			feed_search = SearchSoundCloud(search_arguments)
			feed_search.SearchPageToFeed()
			result_url = feed_search.FeedToUrl()
		expected_url = "http://feeds.soundcloud.com/users/soundcloud:users:26187934/sounds.rss"
		self.assertEqual( result_url, expected_url)

		#optionally tests if the url has been pasted succesfully to clipboard
		try:
			import pyperclip
		except ImportError:
			pass
		else:
			self.assertEqual( pyperclip.paste(), expected_url)

	#integration test
	@patch("builtins.input", return_value="1")
	def test_sc2rss_integration(self, *args, **kwargs):
		search_arguments = ["studio404", "paris"]
		with patch('sys.stdout', new=StringIO()) as silence_stdout:
			feed_search = SearchSoundCloud(search_arguments)
			feed_search.SearchPageToFeed()
			result_url = feed_search.FeedToUrl()
		expected_url = "http://feeds.soundcloud.com/users/soundcloud:users:26187934/sounds.rss"
		self.assertEqual( result_url, expected_url)

		#optionally tests if the url has been pasted succesfully to clipboard
		try:
			import pyperclip
		except ImportError:
			pass
		else:
			self.assertEqual( pyperclip.paste(), expected_url)

if __name__ == "__main__":
	unittest.main()
