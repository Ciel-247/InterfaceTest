# -*- coding: utf-8 -*-
'''
用例执行相关功能
'''
import sqlalchemy,requests,re,openpyxl,datetime
from sqlalchemy import Column, String, create_engine, MetaData,Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def test_execute(caseId):
    pass

def import_case_into_sqlite(PATH,sheet_name):
    #首先连接数据库定义表
    engine = create_engine('sqlite:///E:\\GitHubProject\\InterfaceTest\\data\\AutoTest.db', echo = True)
    metadata = MetaData(engine)
    # <editor-fold desc="define test_case_table">
    #采用新定义表的方法
    # test_case_table = Table('test_case', metadata,
    #                         Column("sheet_name", String)
    #                         Column("caseId", String, primary_key = True)
    #                         Column("class_name", String)
    #                         Column("func_name", String)
    #                         Column("caseDescription", String)
    #                         Column("http_method", String)
    #                         Column("uri", String)
    #                         Column("headers", String)
    #                         Column("body", String)
    #                         Column("kwassert", String)
    #                         Column("correlations", String)
    #                         Column("if_exec", String)
    #                         Column("create_time", String))
    # </editor-fold>
    test_case_table = Table('test_case', metadata, autoload=True)
    result_table = Table('result', metadata, autoload = True)
    metadata.create_all()
    DBsession = sessionmaker(engine)
    session = DBsession()
    #然后从Excel中读取数据，用于放入数据库
    work_book = openpyxl.load_workbook(PATH)
    ws = work_book.get_sheet_by_name(sheet_name)
    for row_cont in ws.iter_rows(min_row = 2):#遍历excel的每一行放入一个dict
        params_dict = dict(
            sheet_name = sheet_name,
            caseId = row_cont[0].value,
            class_name = row_cont[1].value,
            func_name=row_cont[2].value,
            caseDescription=row_cont[3].value,
            http_method=row_cont[4].value,
            uri=row_cont[5].value,
            headers=row_cont[6].value,
            body=row_cont[7].value,
            kwassert=row_cont[8].value,
            correlations=row_cont[9].value,
            if_exec = row_cont[10].value,
            create_time = datetime.datetime.now()
        )
        session.add(test_case_data(**params_dict))#把params_dict放入test_case_data类插入test_case表中
        session.commit()



    # print([c.name for c in test_case_table.columns])
    # print([c.name for c in result_table.columns])

def parse_correlation():
    pass

def get_checkPoint():
    pass

def get_response():
    pass


Base = declarative_base()
class test_case_data(Base):#test_case表定义表结构，用于直接将dict插入数据库中
    #表名
    __tablename__ = "test_case"
    #表结构
    sheet_name = Column(String)
    caseId = Column(String, primary_key = True)
    class_name = Column(String)
    func_name = Column(String)
    caseDescription = Column(String)
    http_method = Column(String)
    uri = Column(String)
    headers = Column(String)
    body= Column(String)
    kwassert = Column(String)
    correlations = Column(String)
    if_exec = Column(String)
    create_time = Column(String)

    def __init__(self, sheet_name, caseId, class_name, func_name, caseDescription, http_method, uri, headers, body, kwassert, correlations, if_exec, create_time):
        self.sheet_name = sheet_name
        self.caseId = caseId
        self.class_name = class_name
        self.func_name = func_name
        self.caseDescription = caseDescription
        self.http_method = http_method
        self.uri = uri
        self.headers = headers
        self.body = body
        self.kwassert = kwassert
        self.correlations = correlations
        self.if_exec = if_exec
        self.create_time = create_time

if __name__ == "__main__":
    import_case_into_sqlite("../data/test-case_v1116_v2.xlsx","suites-test_zj_ysbqc")