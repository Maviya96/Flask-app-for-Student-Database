import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


# We will add classes here
class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    dob= Column(String(250))
    amount_due = Column(Integer)

    @property
    def serialize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'amount_due': self.amount_due,
            'id': self.id,
            'dob': self.dob,
        }


# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///students-collection.db')
Base.metadata.create_all(engine)