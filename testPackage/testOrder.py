# -*- coding:utf-8 -*-
'''
Author  :   lesq
Project :   testOrder
'''

import unittest

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_case1(self):
        print("----case1----")

    def test_case3(self):
        print("----case3----")

    def test_case2(self):
        print("----case2----")

    def tearDown(self):
        print('Test over')

if __name__ == '__main__':
    unittest.main()


    # # by suite
    # suite=unittest.TestSuite()
    # suite.addTest(Test('test_case2'))
    # suite.addTest(Test('test_case1'))
    # suite.addTest(Test('test_case3'))
    # runner=unittest.TextTestRunner()
    # runner.run(suite)




