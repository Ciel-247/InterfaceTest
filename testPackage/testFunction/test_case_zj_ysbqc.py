# -*- coding: utf-8 -*-

""" 测试工具自动生成的case """

import unittest,requests
import create_case_func as func
import Params

class test_case_zj_ysbqc(unittest.TestCase):
    def setUp(self):
        """ test setup function """


    def tearDown(self):
        """ test case tearDown function """

    def test_case_YSBQC01_1(self):
        method = "GET"
        uri = "http://192.168.149.135:8082/login-web/base/getRsaPublicKey.do"
        Headers_xlsx = None
        Bodys_xlsx = None
        kwassert = '''"success": true'''
        Correlations_xlsx = '''p_name=PublicKey&LB="pk": "&RB="'''
        create_case = func.create_case_func(Headers_xlsx,Bodys_xlsx,str(Correlations_xlsx))
        Headers = create_case.parse_headers()
        response = requests.request(method,uri,headers = Headers)
        Correlations = create_case.parse_correlations()
        print
        Params.Params[Correlations['p_name']] = str(create_case.get_p_name_value(Correlations['p_name'],Correlations['LB'],Correlations['RB'],response.text))
        print ("666        %s's value is :" % Correlations['p_name'],Params[Correlations['p_name']])
        # print (response.text)
        print ("9999    ", Params)
        self.assertIn(str(kwassert), str(response.text))

    def test_case_YSBQC01_2(self):
        print ("7777    ",Params.Params["PublicKey"])

if __name__ == "__main__":
    unittest.main()
