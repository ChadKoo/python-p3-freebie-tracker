from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # one-to-many to 
    freebies = relationship(
        'Freebie',
        back_populates='company',
        cascade='all, delete-orphan'
    )
    # many-to-many s
    devs = relationship(
        'Dev',
        secondary='freebies',
        back_populates='companies'
    )

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        return freebie
    
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()
    

    def __repr__(self):
        return f'<Company {self.name}>'


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

   # one-to-many 
    freebies = relationship(
        'Freebie',
        back_populates='dev',
        cascade='all, delete-orphan'
    )
    # many-to-many 
    companies = relationship(
        'Company',
        secondary='freebies',
        back_populates='devs'
    )

    def received_one(self, item_name):
        # Loop through each freebie this dev owns
        for freebie in self.freebies:
        # If we find one whose name matches, return True immediately
            if freebie.item_name == item_name:
                return True
        # If we finished the loop without finding a match, return False
        return False

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            return freebie
        return None
    
    def __repr__(self):
        return f'<Dev {self.name}>'
    

    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    
    dev     = relationship('Dev',     back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."

    def __repr__(self):
        return f'Freebie(id={self.id}, ' + \
            f'item_name={self.item_name}, ' + \
            f'value={self.value})'

