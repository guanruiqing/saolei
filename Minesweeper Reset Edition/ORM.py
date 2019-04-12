

import contextlib

import sqlalchemy
from sqlalchemy import Column, create_engine, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    name = Column(String, primary_key=True)
    salt_value = Column(String, nullable=False)
    hash_password = Column(String, nullable=False)
    map_setting = Column(String)
    system_map = Column(String)
    player_map = Column(String)
    create_time = Column(DateTime)
    save_time = Column(DateTime)
    step_count = Column(Integer)

engine = create_engine('sqlite:///user.db')

DBsession = sessionmaker(bind=engine)


def Database_Reset():
    '''
    delete table and create table
    '''
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Database_add('Tourist', '0.582452088761414', '37825eaf0b384370ecfab819e507eaa7')
    Database_add('root', '0.7069065476009486', 'a9f8a2492eca40df836313596c9a20a3')
    #root password

def Database_add(name, salt_value, hash_password):
    '''
    add user in database

    Args:
        name: user nanme, a string
        salt_value: a random value, a string
        hsah_password: (Password + salt_value)'s hash value

    Return:
        Whether a boolean value is successfully created

    Raises:
        sqlalchemy.exc.IntegrityError: Username already exists
    '''
    with contextlib.closing(DBsession()) as session:
        session.add(User(name = name,
                         salt_value = salt_value,
                         hash_password = hash_password,
                         map_setting = '""',
                         system_map = '""',
                         player_map = '""',
                         create_time = None,
                         save_time = None,
                         step_count = 0
                        ))
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            return False
        return True


def Database_delete(name):
    '''
    delete user in database

    Args:
        name: user name

    Return:
        Whether a boolean value is successfully deleted (0 or 1)

    Raises:
        None
    '''
    with contextlib.closing(DBsession()) as session:
        status = session.query(User).filter_by(name=name).delete()
        return status


def Database_update(user):
    '''
    update user in databse

    Args:
        user: An instance of the User class, using the return value of the 'database_select' query

    Return:
        Whether a boolean value is successfully saved (0 or 1)

    Raises:
        None: I do not know
    '''
    with contextlib.closing(DBsession()) as session:
        user_dict = {'map_setting':user.map_setting,
                     'system_map':user.system_map,
                     'player_map':user.player_map,
                     'create_time':user.create_time,
                     'save_time':user.save_time,
                     'step_count':user.step_count
                    }
        try:
            status = session.query(User).filter(User.name==user.name).update(user_dict)
        except sqlalchemy.exc.InterfaceError:
            return 'value error'
        except sqlalchemy.exc.InvalidRequestError:
            return 'property error'
        session.commit()
        return status


def Database_select(name):
    '''
    select user in database

    Args:
        name: user name

    Return:
        An instance of the User class

    Raises:
        sqlalchemy.orm.exc.NoResultFound: no found user name
    '''
    with contextlib.closing(DBsession()) as session:
        try:
            user = session.query(User).filter(User.name==name).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        return user


