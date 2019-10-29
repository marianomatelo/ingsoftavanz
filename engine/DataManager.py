#!/usr/bin/python
# -*- coding: utf-8 -*-
### IMPORT LIBRARIES ###
import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dao import Dao


class DataManager(object):
    '''
    Class to manage all access to Database
    '''

    def __init__(self, input_table='None', output_table='None', schema='public'):
        '''
        :param input_table: Name of the historic table
        :param output_table: Name of the table used to save the forecast
        :param schema: database schema
        '''

        try:
            ### REMOTE CONNECTION ###
            if os.name == 'nt':
                self.dao = Dao(host='forecastia.com', port='5432', user='postgres', password='continente7', db='Playground',
                          schema=schema)
            ### LOCAL CONNECTION ###
            else:
                self.dao = Dao(host='localhost', port='5432', user='postgres', password='continente7', db='Playground',
                          schema=schema)

            self.input_table = input_table
            self.output_table = output_table
            self.schema = schema

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            raise Exception('Error Connecting to DB: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))


    def runQueriesDict(self, dao, queryNames=[], queryDict={}):
        '''Runs queries loaded from folder.'''
        try:
            # checks if something in dict
            if len(queryDict) == 0 or len(queryNames) == 0:
                print('No queries to run')
            for qName in queryNames:
                self.runQueries(dao, queryDict[qName])

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            raise Exception('Error running queries dict: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))


    def sqlToRun(self, fileNames):
        '''Returns a list with names of queries to run in a list.
        00 are excluded
        anything but .sql is excluded.'''
        try:
            fileList = []
            for fileName in fileNames:
                if fileName[-4:] == '.sql' and fileName[0:2] != '00':
                    fileList.append(fileName)
            return sorted(fileList)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            raise Exception('Error preparing query list: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))


    def filesInFolder(self, path):
        '''Returns the files inside designated path.
        path: string with the directory.'''
        try:
            # Armo una lista vacia
            flist = []
            # Lee el nombre de las carpetas en path0 y los agrega a fs
            for (dirpath, dirnames, filenames) in os.walk(path):
                if dirpath == path:
                    flist.extend(filenames)
            return flist

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            raise Exception('Error finding files: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))

    def readSQLFile(self, path, fileName):
        '''Reads SQL Queries from a moving_avg.sql file
        Returns a list with queries to run
        '''
        sqlFile = open(os.path.join(path, fileName), 'r')
        sql = sqlFile.read()
        sqlFile.close()
        return sql.split(';')

    def runQueries(self, dao, queryList=[]):
        '''Runs individually each query in a list.'''
        for q in queryList:
            if len(q) > 0 and q != '\n' and q != '' and q != ' ':
                dao.run_query(q)

    def getQueries(self, path):
        try:
            basePath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
            path1 = os.path.join(basePath, path)
            qList = self.sqlToRun(self.filesInFolder(path1))
            return qList
        except Exception as e:
            print('Error getting queries: ' + str(e))
            return False

    def loadQueries(self, pathIni):
        '''Reads all queries in a folder.'''
        try:
            queryNames = self.getQueries(pathIni)
            queryDict = {}
            for q in queryNames:
                queryDict[q] = self.readSQLFile(pathIni, q)
            return queryNames, queryDict

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            raise Exception('Error reading initial queries:', str(e) + ' in line: ' +str(exc_tb.tb_lineno))

    def runFolderQueries(self, dao, folder):

        basePath = os.path.abspath(os.path.join(os.path.dirname(__file__)))

        path = os.path.join(basePath, folder)

        ipQueryNames, ipQueries = self.loadQueries(path)

        self.runQueriesDict(dao, ipQueryNames, ipQueries)