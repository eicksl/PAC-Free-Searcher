import requests
from bs4 import BeautifulSoup
from pacfree_searcher.constants import GOOGLE_SEARCH, SPECS
from pacfree_searcher.campaignsite import CampaignSiteParser


class GoogleParser():
    """Handles the details of sending search requests to google and parsing
    results for info on a specific candidate's stance with regards to PAC
    money."""
    def __init__(self, data):
        """Initializes google search and parsing process using the data for
        the candidate."""
        self.data = data
        if self.data['campaign_url'] is None:
            self.find_campaign_url()
        if self.meets_specs():
            CampaignSiteParser(self.data)


    def find_campaign_url(self):
        """Attempts to find a campaign website via google search and updates
        the candidate's data if found."""
        query = self._get_campaign_url_search_string()
        resp = requests.get(GOOGLE_SEARCH, params={'q': query})
        print(resp.url)
        return
        html = BeautifulSoup(resp.text, 'lxml')
        last_name = self.data['name'].rsplit(' ', 1)[1].lower()
        #print(html.find_all('h3', class_='r'))
        for elem in html.find_all('h3', class_='r'):
            assert elem.next_element.name == 'a'
            url = elem.next_element['href'][7:].split('&sa')[0].lower()
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
        resp = requests.get(GOOGLE_SEARCH, params={'q': query})
        html = BeautifulSoup(resp.text, 'lxml')
        if html.find_all('h3', class_='r'):
            return True
        return False


    def _get_meets_specs_search_string(self):
        """Helper function for `meets_specs`. Constructs a google search
        query parameter string from `self.data` and returns it."""
        str_search = 'site:{} '.format(self.data['campaign_url'])
        for spec in SPECS:
            str_search += '\"{}\" OR '.format(spec)
        return str_search[:-4]
