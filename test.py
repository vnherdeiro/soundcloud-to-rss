#! /usr/bin/python3

import unittest
from unittest.mock import patch
from io import StringIO
from sc2rss import SearchSoundCloud

class Test_sc2rss(unittest.TestCase):
	"""
	Exhaustive test for sc2rss
	"""

	@patch("builtins.input", return_value="1")
	def test_search(self, *args, **kwargs):
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
