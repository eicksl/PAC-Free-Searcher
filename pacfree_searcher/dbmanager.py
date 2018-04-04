from sqlalchemy import and_
from pacfree_searcher.models import Candidate


class DBManager():
    def __init__(self, data, db):
        """Initialize DBManager."""
        self.data = data
        self.db = db
        # The app currently lacks any reliable method of obtaining emails
        self.data['emails'] = None
        if not self.is_in_db():
            self.add_candidate()


    def is_in_db(self):
        """Check if the candidate is already in the database."""
        duplicate = self.db.query(Candidate).filter(and_(
            Candidate.name == self.data['name'],
            Candidate.abbr == self.data['abbr'],
            Candidate.office == self.data['office'])
        ).count()
        assert not duplicate > 1
        return True if duplicate else False


    def add_candidate(self):
        """Add candidate to the database."""
        self.db.add(Candidate(**self.data))
        self.db.commit()
