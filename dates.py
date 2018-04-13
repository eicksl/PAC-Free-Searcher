import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pacfree_searcher.constants import STATES, DATES_SOURCE
from pacfree_searcher.models import Base, PrimaryDate


class DatesParser():
    """Handles the details of parsing the election dates and adding them to
    the database."""
    def __init__(self):
        """Sets up the connection to the database and calls `get_dates`"""
        engine = create_engine('sqlite:///dates.db')
        Base.metadata.bind = engine
        self.db = sessionmaker(bind=engine)()
        self.get_dates()


    def get_dates(self):
        """Finds all primary dates and calls `add_date` to add them to the
        database."""
        resp = requests.get(DATES_SOURCE)
        html = BeautifulSoup(resp.text, 'lxml')
        data = html.find('table').find_all('td')
        state, date = (None, None)
        for i in range(0, len(data)):
            if i % 2 == 0:
                state = data[i].string
                assert date is None
                continue
            date = data[i].string
            entry = {
                'state': state,
                'abbr': STATES[state],
                'date': date
            }
            self.add_entry(entry)
            date = None


    def add_entry(self, entry):
        """Add primary date entry to the database."""
        self.db.add(PrimaryDate(**entry))
        self.db.commit()



DatesParser()
