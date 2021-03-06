import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from pacfree_searcher.constants import FACEBOOK, TWITTER
from pacfree_searcher.dbmanager import DBManager


class CampaignSiteParser():
    """Handles the details of parsing through a candidate's campaign website
    to obtain additional info. Currently it will simply look for and add
    Facebook and Twitter URLs and then pass all the data to `DBManager`."""
    def __init__(self, data, db):
        """Initializes campaign website search process."""
        self.data = data
        self.get_social_media_urls()
        DBManager(self.data, db)


    def get_social_media_urls(self):
        """Grabs Facebook and Twitter URLs from the candidate's homepage."""
        self.data['facebook'] = None
        self.data['twitter'] = None
        try:
            resp = requests.get(self.data['campaign_url'], verify=False)
        except ConnectionError:
            return
        html = BeautifulSoup(resp.text, 'lxml')
        for anchor in html.find_all('a'):
            try:
                url = anchor['href'].lower()
            except KeyError:
                continue
            last_name = self.data['name'].rsplit(' ', 1)[1].lower()
            if last_name in url:
                if FACEBOOK in url:
                    self.data['facebook'] = url
                elif TWITTER in url:
                    self.data['twitter'] = url
