# -*- coding: utf-8 -*-

'''
用例执行文件
'''
import datetime
import unittest
from unittest import TestSuite

from TestCase import testcase_func as func
from util import HTMLTestRunner


class load_tests():
    func.import_case_into_mysql("./data/test-case_v1116_v2.xlsx",
                           "suites-test_zj_ysbqc")  # 先调用程序把PATH路径的用例文件的sheet页的用例导出到sqlite中去
    suite = unittest.defaultTestLoader.discover('',pattern = 'test_*.py')
    print("suite's type is :%s" % type(suite))
    with open('./Report/TestReport.html', 'wb') as files:
        runner = HTMLTestRunner.HTMLTestRunner(
            files,
            title = 'TestReport_{0}'.format(datetime.datetime.now()),
            description = u'自动化接口测试报告'
        )
        runner.run(suite)

if __name__ == "__main__":
    unittest.main()
