#!/usr/bin/env python2
# -*- coding:utf-8 -*-

'''
created by lesq
2017-09-05
学习记录
'''

# class Student(object):
#     def __init__(self,name,score):
#         self.__name = name
#         self.__score = score
#
#     def print_info(self):
#         print '%s: %s' % (self.__name,self.__score)
#
# Sue = Student('Sue',98)
# Sue.print_info()
# Sue.__name = 'Sakky'
# print Sue.__name
# Sue.print_info()

#           学习class结束

########################################################################################################3
#           学习接口测试开始
from flask import Flask,render_template,request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/user/<name>")
# def user(name):
#     return render_template("user.html",name = name)

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "lesq" and password == "123":
            return "<h1>welcome, %s ! </h1>" % username
        else:
            return "<h1>Fail to login.</h1>"


if __name__ == '__main__':
    app.run(debug=True)