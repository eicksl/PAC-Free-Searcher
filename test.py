import unittest
from pacfree_searcher.google import GoogleParser


class DummyGoogleParser(GoogleParser):
    def __init__(self, data):
        self.data = data


class GoogleParserTestCases(unittest.TestCase):
    def setUp(self):
        mock_data = {
            'name': 'Mark McGovern',
            'state': 'New Jersey',
            'abbr': 'NJ',
            'office': 'House-2',
            'campaign_url': None
        }
        self.inst = DummyGoogleParser(mock_data)


    def test_get_campaign_url_search_string(self):
        expected = '''\"Mark McGovern\" \"New Jersey\" House district 2'''
        self.assertEqual(self.inst._get_campaign_url_search_string(), expected)


    def test_find_campaign_url(self):
        self.inst.find_campaign_url()


if __name__ == '__main__':
    unittest.main()
