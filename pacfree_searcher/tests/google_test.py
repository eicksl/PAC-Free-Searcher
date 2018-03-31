import unittest
import sys
sys.path.append('..')
from google import GoogleParser


class DummyGoogleParser(GoogleParser):
    def __init__(self, data):
        self.data = data


class GoogleParserTestCases(unittest.TestCase):
    def test_get_campaign_url_search_string(self):
        mock_data = {
            'name': 'Steely Sterns',
            'state': 'North Dakota',
            'office': 'House-4'
        }
        expected = '''\"Steely+Sterns\"+\"North+Dakota\"+House+district+4'''
        inst = DummyGoogleParser(mock_data)
        self.assertEqual(inst._get_campaign_url_search_string(), expected)



if __name__ == '__main__':
    unittest.main()
