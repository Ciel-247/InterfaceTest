# -*- coding: utf-8 -*-
'''
@ Version : 0.1
@ Author  : lesq
@ File    : LESQ_create_case_func.py
@ Project : AuteTeset
@ Create Time: 2017-11-17
@ Python version : 3.x
'''
import re
class deal_result_func():
    def __init__(self,headers,bodys,correlations):
        self.headers = headers
        self.bodys = bodys
        self.correlations = correlations
        self.p_name = None
        self.LB = None
        self.RB = None
        self.p_names = {}

    def parse_headers(self):
        if self.headers == "None":
            return None
        else:
            return self.headers

    def parse_bodys(self):
        if self.bodys == "None":
            return None
        else:
            return self.bodys

    def parse_correlations(self):
        '''
        解析用例里correlations里面的1行，利用正则表达式截取出p_name,LB,RB并返回，如果correlations为None则返回None
        :return: None or (p_name,LB,RB)
        '''
        if self.correlations == None:
            return None
        self.p_name = ''.join(re.findall(r"p_name=(.+?)&",self.correlations))
        self.LB = ''.join(re.findall(r"&LB=(.+?)&",self.correlations))
        self.RB = ''.join(re.findall(r"&RB=(.+?)",self.correlations))
        # self.LB = "\""
        # self.RB = "\""
        print (self.correlations)
        print ("p_name is : %s \nLB is : %s\nRB is : %s"%(self.p_name, self.LB, self.RB))
        return {"p_name":self.p_name, "LB":self.LB, "RB":self.RB}

    def get_p_name_value(self,p_name,LB,RB,response):
        if p_name == None:
            return None
        regex = str(LB) + ("(.*)") + str(RB)
        print ("regex is :", regex)
        print ("response's type is :",type(response))
        self.p_names[p_name] = ''.join(re.findall(r"%s" % regex ,response))
        print ("888      ",self.p_names[p_name])
        return self.p_names[p_name]
