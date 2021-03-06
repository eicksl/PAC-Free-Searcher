import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from pacfree_searcher.constants import *
from pacfree_searcher.models import Base, Candidate
from pacfree_searcher.google import GoogleParser


class ElectionsParser():
    """Handles the details of parsing through the elections data provider's
    structural and semantic HTML mess to obtain necessary candidate data."""

    def __init__(self):
        """Initializes the ElectionsParser. This effectively initiates the
        the entire application process."""
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        engine = create_engine('sqlite:///candidates.db')
        Base.metadata.bind = engine
        self.db = sessionmaker(bind=engine)()
        self.search_all_states()


    def search_all_states(self):
        print('Starting search...', flush=True)
        for state in STATES.keys():
            time.sleep(2)
            print('\nSearching for candidates in {}...'.format(state), flush=True)
            before = self.db.query(Candidate).count()
            urls = self.get_2018_election_urls(state)
            for url in urls:
                self.search_specific_state(url, state)
            after = self.db.query(Candidate).count()
            print('Added {} candidates to the database.'
                  .format(after - before), flush=True)
        print('\nSearch complete.')


    def get_2018_election_urls(self, state):
        """
        :param state: US state
        :type state: string
        :return: Senate and House election URLs
        :rtype: tuple
        """
        state = state.replace(' ', '_')
        resp = requests.get(ELECTIONS_HOME + state)
        html = BeautifulSoup(resp.text, 'lxml')
        anchors = html.select('#state-portal-election-box')[0].p.find_all('a')
        senate_url, house_url = (None, None)
        for anchor in anchors:
            if anchor.string:
                if 'U.S. Senate' in anchor.string:
                    senate_url = ELECTIONS_HOME + anchor['href'][1:]
                elif 'U.S. House' in anchor.string:
                    house_url = ELECTIONS_HOME + anchor['href'][1:]
        return (senate_url, house_url)


    def search_specific_state(self, base_url, state):
        """
        :param base_url: elections page on which to search
        :param state: US state
        :type base_url: string
        :type state: string
        """
        if base_url is None:
            return
        resp = requests.get(base_url)
        html = BeautifulSoup(resp.text, 'lxml')
        if 'House' in html.find('title').string:
            if state in AT_LARGE_STATES:
                self._get_candidate_data_senate_hal(html, state, hal=True)
            else:
                self._get_candidate_data_house(html, state)
        else:
            self._get_candidate_data_senate_hal(html, state)


    def _get_candidate_data_house(self, html, state):
        """
        :param html: house elections page html for which to parse
        :param state: US state
        :type html: BeautifulSoup object
        :type state: string
        """
        candidate_found = False
        district = None
        for anchor in html.find_all('a'):
            if (anchor.get('title', None)
            and 'Congressional District election, 2018' in anchor['title']
            and anchor.parent.name != 'center'):
                district = anchor.string.split(' ')[1]
            elif anchor.parent.name == 'li' or anchor.parent.name == 'td':
                if (' - Incumbent' in anchor.parent and anchor.string
                or anchor.next_sibling and anchor.next_sibling.name == 'sup'):
                    assert anchor.string is not None and len(anchor.string) > 0
                    assert district is not None
                    candidate_found = True
                    data = {
                        'name': anchor.string,
                        'state': state,
                        'abbr': STATES[state],
                        'office': 'House-' + district,
                        'bp_url': ELECTIONS_HOME + anchor['href'][1:]
                    }
                    self.get_party_and_campaign_url(data)
        assert candidate_found


    def _get_candidate_data_senate_hal(self, html, state, hal=False):
        """
        :param html: senate or hal elections page html for which to parse
        :param state: US state
        :param hal: whether this is a House election for an at-large district
        :type html: BeautifulSoup object
        :type state: string
        :type hal: boolean
        """
        candidate_found = False
        office = 'House-0' if hal else 'Senate-' + SENATE_CLASS
        for anchor in html.find_all('a'):
            if anchor.parent.name == 'li' or anchor.parent.name == 'td':
                if (' - Incumbent' in anchor.parent and anchor.string
                or anchor.next_sibling and anchor.next_sibling.name == 'sup'):
                    assert anchor.string is not None and len(anchor.string) > 0
                    candidate_found = True
                    data = {
                        'name': anchor.string,
                        'state': state,
                        'abbr': STATES[state],
                        'office': office,
                        'bp_url': ELECTIONS_HOME + anchor['href'][1:]
                    }
                    self.get_party_and_campaign_url(data)
        assert candidate_found


    def get_party_and_campaign_url(self, data):
        """
        :param data: elections data for a specific candidate
        :type data: dict
        """
        resp = requests.get(data['bp_url'])
        html = BeautifulSoup(resp.text, 'lxml')
        infobox = html.find('div', class_='infobox person')
        if infobox is None:
            return
        try:
            party = (infobox.find('div', class_='widget-row value-only white')
                    .find('a').string)
            data['party'] = party
        except AttributeError:  # most likely due to withdrawal or death
            return
        contact = infobox.find('a', string='Website')
        data['campaign_url'] = None if not contact else contact['href']
        self.search_google(data)


    def search_google(self, data):
        """Pass data for a specific candidate to `GoogleParser`."""
        GoogleParser(data, self.db)
