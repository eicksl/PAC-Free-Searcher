from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base


class Candidate(Base):
    __tablename__ = 'candidate'

    name = Column(String(250), nullable=False)
    key = Column(Integer, primary_key=True)
    state = Column(String(50), nullable=False)
    abbr = Column(String(2), nullable=False)
    office = Column(String(10), nullable=False)
    party = Column(String(50), nullable=False)
    website = Column(String(250), nullable=False)
    emails = Column(String(250))
    facebook = Column(String(100))
    twitter = Column(String(100))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'state': self.state,
            'abbr': self.abbr,
            'office': self.office,
            'party': self.party,
            'website': self.website,
            'emails': self.emails,
            'facebook': self.facebook,
            'twitter': self.twitter
        }


engine = create_engine('sqlite:///candidates.db')
Base.metadata.create_all(engine)
