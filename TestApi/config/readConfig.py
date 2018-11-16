#coding:utf-8

# ================读取cfg.ini文件设置=================

import os
import configparser

# os.path.realpath(__file__)：返回当前文件的绝对路径
# os.path.dirname()： 返回（）所在目录
cur_path = os.path.dirname(os.path.realpath(__file__)) # 当前文件的所在目录
configPath = os.path.join(cur_path,"cfg.ini") # 路径拼接：/config/cfg.ini
conf = configparser.ConfigParser()
conf.read(configPath,encoding='UTF-8') # 读取/config/cfg.ini 的内容

# get(section,option) 得到section中option的值，返回为string类型
smtp_server = conf.get("email","smtp_server")
sender = conf.get("email","sender")
psw = conf.get("email","psw")
receiver = conf.get("email","receiver")
port = conf.get("email","port")

