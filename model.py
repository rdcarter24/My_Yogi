from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Sequence
import os


# Use connection function below when initializing database.
# Comment 13 though 21 out when using connection function
ENGINE = None
Session = None

if os.environ.get('HEROKU_POSTGRESQL_VIOLET_URL'):
    ENGINE = create_engine(os.environ.get('HEROKU_POSTGRESQL_VIOLET_URL'), echo=False)
else:
    ENGINE = create_engine("sqlite:///yoga.db", echo=False)

session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

Base = declarative_base()

#comment 26 through 27 out when using connect function below
Base.query = session.query_property()
Base.metadata.create_all(ENGINE)


#Class declaration
class Asana(Base):
    __tablename__ = "asanas"

    id = Column(Integer, Sequence('asanas_id_seq', start=1, increment=1), primary_key=True)
    name = Column(String(64), nullable=False)
    image = Column(String(64), nullable=True)
    position = Column(String(1), nullable=True)
    sub_routine = Column(String(64), nullable=True)
    breaths = Column(Integer, nullable=True)
    variance = Column(Integer, nullable=True)


class Flow(Base):
    __tablename__ = "flows"

    id = Column(Integer, primary_key=True)
    asana_id = Column(Integer, ForeignKey('asanas.id'))
    flow_id = Column(Integer, nullable=False)
    order =Column(Integer, nullable=False)
    breaths = Column(Integer, nullable=True)

    asana = relationship("Asana", backref=backref("flows", order_by=id))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence('users_id_seq', start=1, increment=1), primary_key=True)
    username = Column(String(64), nullable= False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)

class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable= True)
    user_id = Column(Integer, ForeignKey('users.id'))
    breaths = Column(Integer, nullable=True)

    user = relationship("User", backref=backref("routines", order_by=id))

#reference by asana id insead of name, and change move to asana
class Routine_Asana(Base):
    __tablename__ = "routine_asanas"

    id = Column(Integer, primary_key=True)
    asana_id = Column(Integer, ForeignKey('asanas.id'))
    routine_id = Column(Integer, ForeignKey('routines.id'))
    order = Column(Integer, nullable=False)
    breaths = Column(Integer, nullable=True)
    sub_routine = Column(String(64), nullable=True)

    routine = relationship("Routine",backref=backref("routine_asanas", order_by=id))
    asana = relationship("Asana",backref=backref("routine_asanas", order_by=id))

class Feedback_Asana(Base):
    __tablename__ = "feedback_asanas"

    id = Column(Integer, primary_key=True)
    asana_id = Column(Integer, ForeignKey('asanas.id'))
    routine_id = Column(Integer, ForeignKey('routines.id'))
    sub_routine = Column(String(64), nullable=True)
    rating = Column(Integer, nullable=False)

    routine = relationship("Routine",backref=backref("feedback_asanas", order_by=id))
    asana = relationship("Asana",backref=backref("feedback_asanas", order_by=id))

#use connect function when initializing database
# def connect():
#     global ENGINE
#     global Session

#     if os.environ.get('HEROKU_POSTGRESQL_VIOLET_URL'):
#         ENGINE = create_engine(os.environ.get('HEROKU_POSTGRESQL_VIOLET_URL'), echo=False)
#     else:
#         ENGINE = create_engine("sqlite:///yoga.db", echo=False)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()