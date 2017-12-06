# -*- coding: utf-8 -*-

'''
用例执行文件
'''
import unittest
import logging
from TestCase import testcase_func as func

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)

class test_case_zj_ysbqc(unittest.TestCase):
    def setUp(self):
        """ test setup function """

    def tearDown(self):
        """ test case tearDown function """

    def test_case_YSBQC01_1(self):
        caseId = "YSBQC01_1"
        func.test_execute("suites-test_zj_ysbqc", caseId)#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("suites-test_zj_ysbqc", caseId)#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))
        check_point = func.get_checkPoint("suites-test_zj_ysbqc", caseId)
        if check_point != "None":
            self.assertIn(func.get_checkPoint("suites-test_zj_ysbqc", caseId),func.get_response("suites-test_zj_ysbqc", caseId))

    def test_case_YSBQC01_2(self):
        caseId = "YSBQC01_2"
        func.test_execute("suites-test_zj_ysbqc", caseId)#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("suites-test_zj_ysbqc", caseId)#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))
        check_point = func.get_checkPoint("suites-test_zj_ysbqc", caseId)
        if check_point != "None":
            self.assertIn(func.get_checkPoint("suites-test_zj_ysbqc", caseId),func.get_response("suites-test_zj_ysbqc", caseId))
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))

    def test_case_YSBQC01_3(self):
        caseId = "YSBQC01_3"
        func.test_execute("suites-test_zj_ysbqc", caseId)#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("suites-test_zj_ysbqc", caseId)#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))
        check_point = func.get_checkPoint("suites-test_zj_ysbqc", caseId)
        if check_point != "None":
            self.assertIn(func.get_checkPoint("suites-test_zj_ysbqc", caseId),func.get_response("suites-test_zj_ysbqc", caseId))


    def test_case_YSBQC01_4(self):
        caseId = "YSBQC01_4"
        func.test_execute("suites-test_zj_ysbqc", caseId)#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("suites-test_zj_ysbqc", caseId)#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))
        check_point = func.get_checkPoint("suites-test_zj_ysbqc", caseId)
        if check_point != "None":
            self.assertIn(func.get_checkPoint("suites-test_zj_ysbqc", caseId),func.get_response("suites-test_zj_ysbqc", caseId))

    def test_case_YSBQC01_5(self):
        caseId = "YSBQC01_5"
        func.test_execute("suites-test_zj_ysbqc", caseId)#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("suites-test_zj_ysbqc", caseId)#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))
        check_point = func.get_checkPoint("suites-test_zj_ysbqc", caseId)
        if check_point != "None":
            self.assertIn(func.get_checkPoint("suites-test_zj_ysbqc", caseId),func.get_response("suites-test_zj_ysbqc", caseId))

    def test_case_YSBQC01_6(self):
        caseId = "YSBQC01_6"
        func.test_execute("suites-test_zj_ysbqc", caseId)#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("suites-test_zj_ysbqc", caseId)#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))
        check_point = func.get_checkPoint("suites-test_zj_ysbqc", caseId)
        if check_point != "None":
            self.assertIn(func.get_checkPoint("suites-test_zj_ysbqc", caseId),"666")

    def test_case_YSBQC01_7(self):
        caseId = "YSBQC01_7"
        func.test_execute("suites-test_zj_ysbqc", caseId)#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("suites-test_zj_ysbqc", caseId)#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))
        check_point = func.get_checkPoint("suites-test_zj_ysbqc", caseId)
        if check_point != "None":
            self.assertIn(func.get_checkPoint("suites-test_zj_ysbqc", caseId),func.get_response("suites-test_zj_ysbqc", caseId))
        

    def test_case_YSBQC01_8(self):
        caseId = "YSBQC01_8"
        func.test_execute("suites-test_zj_ysbqc", caseId)#执行第一条用例，执行的时候需要顺便把请求和返回写入日志文件中，最好记录在数据库里面
        func.parse_correlation("suites-test_zj_ysbqc", caseId)#解析并更新第一条用例的关联在数据库里面遍历所有可能出现关联的地方
        print(func.get_report_log("suites-test_zj_ysbqc", caseId))
        check_point = func.get_checkPoint("suites-test_zj_ysbqc", caseId)
        if check_point != "None":
            self.assertIn(func.get_checkPoint("suites-test_zj_ysbqc", caseId),func.get_response("suites-test_zj_ysbqc", caseId))
