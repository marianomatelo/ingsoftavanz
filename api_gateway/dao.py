#!/usr/bin/env python
"""
Simple Data Access Object
"""

import pandas as pd
import sqlalchemy
from sqlalchemy.pool import NullPool
import urllib


class Dao(object):
    """Simplified Data Access Object to query Postgres databases
    """

    def __init__(self, host, port, user, password, db, schema='public', engine='psql'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.schema = schema
        self.engine = sqlalchemy.create_engine(self.get_connection_string(engine), poolclass=NullPool)

    def get_connection_string(self, engine):
        if engine == 'psql':
            return 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.user, self.password, self.host, self.port, self.db)

        else:
            params = 'DRIVER={ODBC Driver 17 for SQL Server};' \
                     'SERVER=' + self.host + ';' \
                     'PORT=' + self.port + ';' \
                     'DATABASE=' + self.db + ';' \
                     'UID=' + self.user + ';' \
                     'PWD=' + self.password + ';'

            params = urllib.parse.quote_plus(params)

            return 'mssql+pyodbc:///?odbc_connect=%s' % params

    def get_engine(self):
        return self.engine

    def run_query(self, query):
        with self.engine.connect() as conn:
            if self.schema != 'public':
                conn.execute("SET search_path TO {}, public".format(self.schema))
            conn.execute(query)

    def download_from_query(self, query, index_col=None):
        with self.engine.connect() as conn:
            if self.schema != 'public':
                conn.execute("SET search_path TO {}, public".format(self.schema))
            return pd.read_sql(query, conn, index_col=index_col)

    def upload_from_dataframe(self, df, table_name, if_exists='replace', chunksize=1000000):
        df.to_sql(table_name, self.engine, schema=self.schema, if_exists=if_exists, index=False, chunksize=chunksize,
                  method='multi')