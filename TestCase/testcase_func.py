# -*- coding: utf-8 -*-
'''
用例执行相关功能
'''
import sqlalchemy,requests,re,openpyxl,datetime
from sqlalchemy import Column, String, create_engine, MetaData,Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///E:\\GitHubProject\\InterfaceTest\\data\\AutoTest.db', echo = False)
metadata = MetaData(engine)
DBsession = sessionmaker(engine)

def test_execute(sheet_name,caseId):
    session = DBsession()#
    requests_info = request_info(sheet_name, caseId)#用于确认返回经过parsed的列还是未经过parsed的列
    Headers = requests_info.get_request_headers()
    body = requests_info.get_request_body()
    (http_method, uri) = session.query(test_case_data.http_method,test_case_data.uri).filter(test_case_data.caseId == caseId).one()
    print("333888", Headers,body,http_method,uri)
    response = requests.request(http_method, uri, headers=eval(Headers), data = eval(body))
    params_dict = dict(
        sheet_name = sheet_name,
        caseId = caseId,
        request_headers = Headers,
        request_body = body,
        response_status_code = response.status_code,
        response_cookies = str(response.cookies.items()),
        request_uri = str(response.url),
        response_text = response.text,
        exec_time = datetime.datetime.now()
    )
    session.add(result_data(**params_dict))
    session.commit()

def import_case_into_sqlite(PATH,sheet_name):
    #首先连接数据库定义表
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
    # test_case_table = Table('test_case', metadata, autoload=True)
    # result_table = Table('result', metadata, autoload = True)
    metadata.create_all()
    session = DBsession()
    #然后从Excel中读取数据，用于放入数据库
    work_book = openpyxl.load_workbook(PATH)
    ws = work_book.get_sheet_by_name(sheet_name)
    for row_cont in ws.iter_rows(min_row = 2):#遍历excel的每一行放入一个dict
        params_dict = dict(
            sheet_name = sheet_name,
            caseId = row_cont[0].value,
            class_name = row_cont[1].value,
            func_name = row_cont[2].value,
            caseDescription = row_cont[3].value,
            http_method = row_cont[4].value,
            uri = row_cont[5].value,
            headers = row_cont[6].value,
            parsed_headers = None,
            body = row_cont[7].value,
            parsed_body = None,
            kwassert = row_cont[8].value,
            parsed_kwassert = None,
            correlations = row_cont[9].value,
            parsed_correlations = None,
            if_exec = row_cont[10].value,
            create_time = datetime.datetime.now()
        )
        session.merge(test_case_data(**params_dict))#把params_dict放入test_case_data类插入test_case表中
        session.commit()



    # print([c.name for c in test_case_table.columns])
    # print([c.name for c in result_table.columns])

def parse_correlation(sheet_name, caseId):
    session = DBsession()
    response = session.query(result_data.response_text).filter(result_data.sheet_name == sheet_name, result_data.caseId == caseId).order_by(result_data.exec_time.desc()).all()[0][0]
    # print("123123123", response)
    correlations = session.query(test_case_data).filter(test_case_data.sheet_name == sheet_name, test_case_data.caseId == caseId).one().correlations#根据sheet_name,caseId从数据库查找对应的correlations
    # print("correlations is :",correlations)
    correlations_list = correlations.split("&")#一条用例有多个关联时，通过"&"字符进行分割
    # print(correlations_list)
    correlations_dict = {}#定义一个dict用于存放每个关联，关联名作为key，对应正则表达式作为value
    for item in correlations_list:#通过"="分割每个关联，得到关联dict
        key = item.split("=")[0]
        value = item.split("=")[1]
        correlations_dict[key] = value
    print("!!!!correlations is :", correlations_dict)
    parsed_correlations_dict = {}
    for key in correlations_dict:
        replace_str = "%{" + key + "}"  # 用于正则表达式的匹配，用例中所有需要替换的部分都采取“%{key}”的方式来写的
        parsed_correlations_dict[key] = ''.join(re.findall(r"%s" % correlations_dict[key], response))
        print("houhouhou", parsed_correlations_dict)
    #对dict中的每个关联，遍历该sheet_name下所有的headers,body,kwassert,correlations,如果含有%{key}格式的字符串，则替换为该key对应的value，放入对应parsed_xx列（不要直接修改原有列，这样可以从数据库分析用例的整体过程）
    # <editor-fold desc="各列待替换caseId的dict定义">
    parsing_headers_caseId = {}
    parsing_body_caseId = {}
    parsing_kwassert_caseId = {}
    parsing_correlations_caseId = {}
    # </editor-fold>
    for key in correlations_dict:#对关联dict里面的每一个key去拿到存在key关键字的用例id（相关的四列分别有一个dict，key是关联名，value是caseId，供后续替换）
        #因为使用session.query直接查出来的结果是由tuple组成的list【[(xxxx1,),(xxxx2,)]这样的】，所以用[caseId[0] for caseId in xxx]的方式分别取出tuple的第一个值
        # print(key)
        parsing_headers_caseId[key] = [caseId[0] for caseId in session.query(test_case_data.caseId).filter(test_case_data.headers.like("%%{"+key+"}%")).all()]
        parsing_body_caseId[key] = [caseId[0] for caseId in session.query(test_case_data.caseId).filter(test_case_data.body.like("%%{"+key+"}%")).all()]
        parsing_kwassert_caseId[key] = [caseId[0] for caseId in session.query(test_case_data.caseId).filter(test_case_data.kwassert.like("%%{"+key+"}%")).all()]
        parsing_correlations_caseId[key] = [caseId[0] for caseId in session.query(test_case_data.caseId).filter(test_case_data.correlations.like("%%{" + key + "}%")).all()]
    # print(parsing_headers_caseId,parsing_body_caseId)
    # print("parsing_headers_caseId is : ", parsing_headers_caseId)
    for key in correlations_dict:#对关联dict中的每一个关键字都要处理
        replace_str = "%{" + key + "}"#用于正则表达式的匹配，用例中所有需要替换的部分都采取“%{key}”的方式来写的
        newpat = ''.join(re.findall(r"%s" % correlations_dict[key] ,response))#用于替换的新词，从response中通过correlations_dict[key]的正则表达式来取出
        for value in parsing_headers_caseId[key]:#对所有待替换headers的caseId进行处理
            before = session.query(test_case_data.headers).filter(test_case_data.caseId == value).one()[0]
            after = re.sub(r"%s" % replace_str, newpat, before)
            session.query(test_case_data).filter(test_case_data.caseId == value ).update({test_case_data.parsed_headers : after})
            session.commit()
        for value in parsing_body_caseId[key]:#对所有待替换body的caseId进行处理
            before = session.query(test_case_data.body).filter(test_case_data.caseId == value).one()[0]
            after = re.sub(r"%s" % replace_str, newpat, before)
            session.query(test_case_data).filter(test_case_data.caseId == value).update({test_case_data.parsed_body: after})
            session.commit()
        for value in parsing_kwassert_caseId[key]:#对所有待替换kwassert的caseId进行处理
            before = session.query(test_case_data.kwassert).filter(test_case_data.caseId == value).one()[0]
            after = re.sub(r"%s" % replace_str, newpat, before)
            session.query(test_case_data).filter(test_case_data.caseId == value).update({test_case_data.parsed_kwassert: after})
            session.commit()
        for value in parsing_correlations_caseId[key]:#对所有待替换correlations的caseId进行处理
            before = session.query(test_case_data.correlations).filter(test_case_data.caseId == value).one()[0]
            after = re.sub(r"%s" % replace_str, newpat, before)
            session.query(test_case_data).filter(test_case_data.caseId == value).update({test_case_data.parsed_correlations: after})
            session.commit()

def get_checkPoint(sheet_name, caseId):
    session = DBsession()
    checkPoint = session.query(test_case_data).filter(test_case_data.sheet_name == sheet_name,test_case_data.caseId == caseId).one().kwassert
    print("get_checkPoint is :",checkPoint)
    return checkPoint

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
    parsed_headers = Column(String)
    body= Column(String)
    parsed_body= Column(String)
    kwassert = Column(String)
    parsed_kwassert = Column(String)
    correlations = Column(String)
    parsed_correlations = Column(String)
    if_exec = Column(String)
    create_time = Column(String)

    def __init__(self, sheet_name, caseId, class_name, func_name, caseDescription, http_method, uri, headers, parsed_headers, body, parsed_body, kwassert, parsed_kwassert, correlations, parsed_correlations, if_exec, create_time):
        self.sheet_name = sheet_name
        self.caseId = caseId
        self.class_name = class_name
        self.func_name = func_name
        self.caseDescription = caseDescription
        self.http_method = http_method
        self.uri = uri
        self.headers = headers
        self.parsed_headers = parsed_headers
        self.body = body
        self.parsed_body = parsed_body
        self.kwassert = kwassert
        self.parsed_kwassert = parsed_kwassert
        self.correlations = correlations
        self.parsed_correlations = parsed_correlations
        self.if_exec = if_exec
        self.create_time = create_time

class result_data(Base):#result表定义表结构，用于直接将dict插入数据库中
    #表名
    __tablename__ = "result"
    #表结构
    sheet_name = Column(String)
    caseId = Column(String, primary_key = True)
    request_headers = Column(String)
    request_body = Column(String)
    response_status_code = Column(String)
    response_cookies = Column(String)
    request_uri = Column(String)
    response_text = Column(String)
    exec_time = Column(String)
    def __init__(self, sheet_name, caseId, request_headers, request_body, response_status_code, response_cookies, request_uri, response_text, exec_time):
        self.sheet_name = sheet_name
        self.caseId = caseId
        self.request_headers = request_headers
        self.request_body = request_body
        self.response_status_code = response_status_code
        self.response_cookies = response_cookies
        self.request_uri = request_uri
        self.response_text = response_text
        self.exec_time = exec_time

class request_info(object):
    def __init__(self, sheet_name, caseId):
        self.sheet_name = sheet_name
        self.caseId = caseId
        self.session = DBsession()

    def get_request_headers(self):
        (headers, parsed_headers) = self.session.query(test_case_data.headers, test_case_data.parsed_headers).filter(test_case_data.sheet_name == self.sheet_name,test_case_data.caseId == self.caseId).one()
        if parsed_headers != None:
            return parsed_headers
        else:
            return headers

    def get_request_body(self):
        (body, parsed_body) = self.session.query(test_case_data.body,test_case_data.parsed_body).filter(test_case_data.sheet_name == self.sheet_name, test_case_data.caseId == self.caseId).one()
        if parsed_body != None:
            return parsed_body
        else:
            return body

    def get_request_kwassert(self):
        (kwassert, parsed_kwassert) = self.session.query(test_case_data.kwassert, test_case_data.parsed_kwassert).filter(test_case_data.sheet_name == self.sheet_name, test_case_data.caseId == self.caseId).one()
        if parsed_kwassert != None:
            return parsed_kwassert
        else:
            return kwassert

    def get_request_correlations(self):
        (correlations, parsed_correlations) = self.session.query(test_case_data.correlations, test_case_data.parsed_kwassert).filter(test_case_data.sheet_name == self.sheet_name, test_case_data.caseId == self.caseId).one()
        if parsed_correlations != None:
            return parsed_correlations
        else:
            return correlations



if __name__ == "__main__":
    import_case_into_sqlite("../data/test-case_v1116_v2.xlsx","suites-test_zj_ysbqc")
    for i in range (1,8):
        print(i)
        caseId = "YSBQC01_" + str(i)
        test_execute("suites-test_zj_ysbqc", caseId)
        parse_correlation("suites-test_zj_ysbqc",caseId)
