#coding:utf-8

import sqlite3

DB_PATH = 'stock.db'

class DAO(object):
    ''' Data Access Object to put record into sqlite db '''
    def __init__(self):
        pass
    
    def get_dbname(self):
        return DB_PATH
    
    def connect(self):
        self.cx = sqlite3.connect(DB_PATH)
        self.cu = self.cx.cursor()
        
    def create_db(self):
        sql_str = 'create table if not exists stock_summary(id integer primary key, name varchar(20))'
        self.cu.execute(sql_str)
        
        sql_str = 'create table if not exists stock_level1(id integer primary key AUTOINCREMENT, code varchar(20), \
        date date, open double, high double, close double, low double, volume double, turnover double \
        )'
        self.cu.execute(sql_str)
        
    def insert_instrument(self, record):
        sql_str = 'insert into stock_summary(id, name) values (?, ?)'
        self.cu.execute(sql_str, record)
        
    def insert_trade(self, trade_record):
        sql_str = 'insert into stock_level1(code, date, open, high, close, low, volume, turnover) values \
        (?, ?, ?, ?, ?, ?, ?, ?)'
        self.cu.execute(sql_str, trade_record)
        
    def commit(self):
        self.cx.commit()

