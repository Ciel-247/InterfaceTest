# -*- coding: utf-8 -*-

'''
用例执行文件
'''

import unittest,requests
from TestCase import testcase_func as func

class test_case_zj_ysbqc(unittest.TestCase):
    def setUp(self):
        """ test setup function """

    def tearDown(self):
        """ test case tearDown function """

    def test_case_YSBQC01_1(self):
        func.test_execute("01")#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("01")#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        self.assertIn("这里放用例里面的检查点","这里函数返回01用例的结果")  # 断言验证检查点

if __name__ == "__main__":
    func.import_case_into_sqlite("PATH","sheet")#先调用程序把PATH路径的用例文件的sheet页的用例导出到sqlite中去