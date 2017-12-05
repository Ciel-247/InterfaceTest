# -*- coding: utf-8 -*-

""" 测试工具自动生成的case """

import unittest,requests,openpyxl
import deal_result_func as func
import Params

class test_case_zj_ysbqc(unittest.TestCase):
    def setUp(self):
        """ test setup function """
        self.work_book = openpyxl.load_workbook("case_file/test-case_v1116.xlsx")
        self.ws = self.work_book.get_sheet_by_name("suites-test_zj_ysbqc")

    def tearDown(self):
        """ test case tearDown function """

    def test_case_YSBQC01_1(self):

        # <editor-fold desc="从Excel读取第一条用例相关数据">
        caseId = self.ws.cell("A2").value
        class_Name = self.ws.cell("B2").value
        func_Name = self.ws.cell("C2").value
        caseDescription = self.ws.cell("D2").value
        http_method = self.ws.cell("E2").value
        uri = self.ws.cell("F2").value
        Headers_xlsx = self.ws.cell("G2").value
        Bodys_xlsx = self.ws.cell("H2").value
        kwassert = self.ws.cell("I2").value
        Correlations_xlsx = self.ws.cell("J2").value
        print(caseId,http_method,http_method,uri,Headers_xlsx,Bodys_xlsx,kwassert,Correlations_xlsx)
        # </editor-fold>

        create_case = func.deal_result_func(Headers_xlsx,Bodys_xlsx,str(Correlations_xlsx))#调用deal_result_func方法生成该条用例实例
        Headers = create_case.parse_headers()#解析Excel的Headers
        response = requests.request(http_method,uri,headers = Headers)#发送请求
        Correlations = create_case.parse_correlations()#解析关联，返回值为p_name，LB，RB
        # print("2323232",Correlations)
        Params.Params[Correlations['p_name']] = str(create_case.get_p_name_value(Correlations['p_name'],Correlations['LB'],Correlations['RB'],response.text))#通过关联的左右边界，从response中截取出关联变量的值
        print ("666        %s's value is :" % Correlations['p_name'],Params.Params[Correlations['p_name']])
        # print (response.text)
        self.assertIn(str(kwassert), str(response.text))#断言验证检查点

    def test_case_YSBQC01_2(self):
        print ("7777    ",Params.Params["PublicKey"])

if __name__ == "__main__":
    unittest.main()
