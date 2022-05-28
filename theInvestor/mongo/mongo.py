from pymongo import MongoClient
from logger.logger import log

class Mongo():

    # consts
    FIND = 'find'
    INSERT = 'insert'
    COUNT = 'count'
    PATH = 'mongodb://localhost:27017'

    def __init__(self, DBName: str) -> None:
        self.DBName = DBName
        self.db = self.__DBConnection()

        log.debug('Mongo initiliazed')

    def __getMongoClient(self):
        log.debug('Creating MongoClient')
        return MongoClient(Mongo.PATH)

    def __DBConnection(self):
        log.debug(f'Connecting to DB - {self.DBName}')
        return self.__getMongoClient()[self.DBName]

    def __tableConnection(self, tableName: str):
        log.debug(f'Connecting to collection - {tableName}')
        return self.db[tableName]

    def runQuery(self, tableName: str, action: str, queryWhere: dict = {}, querySelect: dict = {}) -> dict:
        action = action.lower()
        collection = self.__tableConnection(tableName)
        if querySelect:
            log.info(f'Query: db.{tableName}.{action}({queryWhere}, {querySelect})')
        else:
            log.info(f'Query: db.{tableName}.{action}({queryWhere})')


        if action == Mongo.FIND:
            response = collection.find(queryWhere, querySelect)
        elif action == Mongo.INSERT:
            response = collection.insert(queryWhere)
        elif action == Mongo.COUNT:
            response = collection.count(queryWhere)
        else:
            log.error('Action not found')
            return False

        for dict in response:
            log.debug(dict)
            return(dict)

