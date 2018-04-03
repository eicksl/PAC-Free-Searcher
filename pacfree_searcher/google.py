import requests
from pacfree_searcher.constants import *
from pacfree_searcher.campaignsite import CampaignSiteParser


class GoogleParser():
    """Handles the details of sending search requests to google and parsing
    results for info on a specific candidate's stance with regards to PAC
    money."""
    def __init__(self, data, db):
        """Initializes google search and parsing process using the data for
        the candidate."""
        self.data = data
        if self.data['campaign_url'] is None:
            self.find_campaign_url()
        if self.meets_specs():
            CampaignSiteParser(self.data, db)


    def find_campaign_url(self):
        """Attempts to find a campaign website via google search and updates
        the candidate's data if found."""
        query = self._get_campaign_url_search_string()
        params = {
            'key': GOOGLE_KEY,
            'cx': GOOGLE_CX,
            'q': query
        }
        resp = requests.get(GOOGLE_SEARCH, params)
        last_name = self.data['name'].rsplit(' ', 1)[1].lower()
        for item in resp.json()['items']:
            url = item['link'].lower()
            split_url = self._split_homepage(url)
            if last_name in split_url:
                self.data['campaign_url'] = split_url
                break


    def _get_campaign_url_search_string(self):
        """Helper function for `find_campaign_url`. Constructs a google search
        query parameter string from `self.data` and returns it."""
        office = self.data['office'].split('-')
        str_search = '\"{}\" \"{}\" {}'.format(
                self.data['name'], self.data['state'], office[0])
        if office[0] == 'House':
            str_search += ' district ' + office[1]
        return str_search


    def _split_homepage(self, url):
        """Helper function for `find_campaign_url`. Truncates the passed URL
        after a top-level domain identifier such as `.com` and returns the
        truncated string. If a top-level domain identifier cannot be found,
        an empty string is returned."""
        domains = [
            '.com', '.net', '.org', '.gov', '.edu', '.info', '.io', '.us'
        ]
        split = False
        for domain in domains:
            if domain in url:
                url = url.split(domain)[0] + domain
                split = True
                break
        if split:
            return url
        return ''


    def meets_specs(self):
        """Determines whether a candidate's campaign website includes language
        about corporate PAC money or money in politics and therefore meets the
        specifications required to be added to the database."""
        if self.data['campaign_url'] is None:
            return False
        query = self._get_meets_specs_search_string()
        params = {
            'key': GOOGLE_KEY,
            'cx': GOOGLE_CX,
            'q': query
        }
        resp_json = requests.get(GOOGLE_SEARCH, params).json()
        results = int(resp_json['searchInformation']['totalResults'])
        if results > 0:
            # Google's Custom Search API sometimes returns results despite no
            # direct matches in `SPECS`. Iterate over the result items and
            # confirm that at least one item in `SPECS` was matched.
            for item in resp_json['items']:
                for spec in SPECS:
                    if spec in item['snippet']:
                        return True
        return False


    def _get_meets_specs_search_string(self):
        """Helper function for `meets_specs`. Constructs a google search
        query parameter string from `self.data` and returns it."""
        str_search = 'site:{} '.format(self.data['campaign_url'])
        for spec in SPECS:
            str_search += '\"{}\" OR '.format(spec)
        return str_search[:-4]
