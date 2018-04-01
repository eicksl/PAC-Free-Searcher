#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
#from pacfree_hunt.models import Base, Candidate
from pacfree_searcher.constants import *
from pacfree_searcher.google import GoogleParser
import time
import requests


#engine = create_engine('sqlite:///candidates.db')
#Base.metadata.bind = engine
#session = sessionmaker(bind=engine)()


class ElectionsParser():
    """Handles the details of parsing through the elections data provider's
    structural and semantic HTML mess to obtain necessary candidate data."""

    def __init__(self):
        """Initializes the ElectionsParser. This effectively initiates the
        the entire application process."""
        #self.get_candidate_data('XXXXXX/United_States_House_of_Representatives_elections_in_New_Jersey,_2018', 'New Jersey')
        pass
        

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
        urls = html.select('#state-portal-election-box')[0].p.find_all('a')
        senate_url = ELECTIONS_HOME + urls[1]['href']
        house_url = ELECTIONS_HOME + urls[2]['href']
        return (senate_url, house_url)


    def get_candidate_data(self, base_url, state):
        """
        :param base_url: elections page on which to search
        :param state: US state
        :type base_url: string
        :type state: string
        """
        resp = requests.get(base_url)
        html = BeautifulSoup(resp.text, 'lxml')
        house_title = ('United States House of Representatives elections in '
                       '{}, 2018 - elections').format(state)
        if html.find('title', string=house_title):
            self._get_candidate_data_house(html, state)
        else:
            self._get_candidate_data_senate(html, state)


    def _get_candidate_data_house(self, html, state):
        """
        :param html: house elections page html for which to parse
        :param state: US state
        :type html: BeautifulSoup object
        :type state: string
        """
        district = None
        for anchor in html.find_all('a'):
            if (anchor.get('title', None)
            and 'Congressional District election, 2018' in anchor['title']
            and anchor.parent.name != 'center'):
                district = anchor.string.split(' ')[1]
            elif anchor.parent.name == 'li':
                if (' - Incumbent' in anchor.parent
                or anchor.next_sibling and anchor.next_sibling.name == 'sup'):
                    assert district is not None
                    data = {
                        'name': anchor.string,
                        'state': state,
                        'abbr': STATES[state],
                        'office': 'House-' + district,
                        'bp_url': ELECTIONS_HOME + anchor['href']
                    }
                    self.get_party_and_campaign_url(data)


    def _get_candidate_data_senate(self, html, state):
        """
        :param html: senate elections page html for which to parse
        :param state: US state
        :type html: BeautifulSoup object
        :type state: string
        """
        for elem in html.find_all('li'):
            if (not dict(elem.attrs).get('class', None)
            and elem.next_element.name == 'a'):
                if (elem.next_element.next_sibling
                and elem.next_element.next_sibling.name == 'sup'
                or ' - Incumbent' in elem):
                    data = {
                        'name': elem.next_element.string,
                        'state': state,
                        'abbr': STATES[state],
                        'office': 'Senate-' + SENATE_CLASS,
                        'bp_url': ELECTIONS_HOME + elem.next_element['href']
                    }
                    self.get_party_and_campaign_url(data)


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
        GoogleParser(data)
