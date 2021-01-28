import pymongo
from pymongo import MongoClient
class dbs:
    con=None
    db=None
    def __init__(self):
        self.con=MongoClient("mongodb+srv://raj1234:raj1234@cluster0.bfodi.mongodb.net/sample_airbnb?retryWrites=true&w=majority")
        self.db=self.con.get_database("soham_db")
    def setrecord(self):
        record=self.db
        return record