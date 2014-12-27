#!/usr/bin/python

#coding:utf-8

import unittest
from dao.dao import DAO
from datasource.sinads import SinaDS
import os

class Test(unittest.TestCase):

    def setUp(self):
        if os.path.exists('stock.db'):
            os.remove('stock.db')
            
        self.dao = DAO()
        self.dao.connect()
        self.dao.create_db()
        
        self.ds = SinaDS()

    def tearDown(self):
        self.dao.commit()


    def testExtract(self):
        for item in self.ds.get_reference():
            self.dao.insert_instrument(item)
        
        for record in self.ds.get_trade_history('600000'):
            print ['600000'] + record
            self.dao.insert_trade(tuple(['600000'] + record))


if __name__ == "__main__":
    unittest.main()
