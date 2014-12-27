#coding:utf-8

import unittest
from sinads import SinaDS

class Test(unittest.TestCase):


    def setUp(self):
        self.ds = SinaDS()


    def tearDown(self):
        pass


    def testName(self):
        i = self.ds.get_trade_history(603998)
        self.ds.export(i)


if __name__ == "__main__":
    unittest.main()