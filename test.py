import unittest
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pacfree_searcher.google import GoogleParser
from pacfree_searcher.campaignsite import CampaignSiteParser


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
        self.inst.find_campaign_url()
        self.assertEqual(self.inst._get_campaign_url_search_string(), expected)


    def test_find_campaign_url(self):
        expected = 'http://www.markmcgovern.com'
        self.inst.find_campaign_url()
        self.assertEqual(self.inst.data['campaign_url'], expected)


    def test_get_meets_specs_search_string(self):
        #self.inst.data['campaign_url'] = 'http://www.bernie.org'
        #print(self.inst._get_meets_specs_search_string())
        pass



    def test_meets_specs(self):
        self.inst.data['campaign_url'] = 'http://www.markmcgovern.com'
        self.assertEqual(self.inst.meets_specs(), False)
        self.inst.data['campaign_url'] = 'https://www.paulajean2018.com'
        self.assertEqual(self.inst.meets_specs(), True)


class DummyCampaignSiteParser(CampaignSiteParser):
    def __init__(self, data):
        self.data = data


class CampaignSiteParserTestCases(unittest.TestCase):
    def setUp(self):
        mock_data = {
            'name': 'Peter Jacob',
            'state': 'New Jersey',
            'abbr': 'NJ',
            'office': 'House-7',
            'campaign_url': 'http://www.jacob2018.com'
        }
        self.inst = DummyCampaignSiteParser(mock_data)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


    def test_get_social_media_urls(self):
        self.inst.get_social_media_urls()
        facebook = 'https://www.facebook.com/peterjacobnj/'
        twitter = 'https://twitter.com/peterjacobnj'
        self.assertEqual(self.inst.data['facebook'], facebook)
        self.assertEqual(self.inst.data['twitter'], twitter)



if __name__ == '__main__':
    unittest.main()
