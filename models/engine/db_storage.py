#!/usr/bin/python3
"""
Involves the category StorageDB
"""

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

categories = {"Amenity": Amenity, "City": City,
              "Place": Place, "Review": Review, "State": State, "User": User}


class StorageDB:
    """collaborates with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Create a StorageDB instance"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def everything(self, cls=None):
        """inquiry on the present database session"""
        new_dict = {}
        for clss in categories:
            if cls is None or cls is categories[clss] or cls is clss:
                objs = self.__session.query(categories[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def addition(self, obj):
        """include the entity in the present database session"""
        self.__session.add(obj)

    def record(self):
        """confirm all changes of the present database session"""
        self.__session.commit()

    def eliminate(self, obj=None):
        """remove from the present database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload_data(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def shutdown(self):
        """invoke the remove() method on the private session attribute"""
        self.__session.remove()

    # Include retrieve function
    def obtain(self, cls, id):
        """A procedure to get one object"""
        if cls in categories.values() and id and type(id) == str:
            resource = self.everything(cls)
            for key, value in resource.items():
                if key.split(".")[1] == id:
                    return value
        return None

    # Include calculate function
    def calculate(self, cls=None):
        """A procedure to determine the quantity of entities in storage"""
        resource = self.everything(cls)
        if cls in categories.values():
            resource = self.everything(cls)
        return len(resource)

