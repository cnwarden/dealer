#coding:utf-8

import unittest
import os
from dao import DAO


class Test(unittest.TestCase):

    def setUp(self):
        self.dao = DAO()
        self.dao.connect()

    def tearDown(self):
        self.dao.commit()

    def testCreation(self):
        self.dao.create_db()

    def testInsertInstrument(self):
        self.dao.insert_instrument(('600000', u'浦发银行'))

if __name__ == "__main__":
    unittest.main()