# coding:utf-8

import unittest
import requests
import os,sys


cur_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,cur_path)
from db_fixture import test_data

class TestAddEvent(unittest.TestCase):
    """添加发布会"""
    def setUp(self):
        self.base_url = "http://47.93.185.38:8000/api/add_event/"

    def tearDown(self):
        print("")

    def test_add_event_all_null(self):
        """所有参数为空添加"""
        payload = {"eid":"","name":"","limit2":"","address":"","start_time":""}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result["status"],10021)
        self.assertEqual(self.result["message"],"parameter error")

    def test_add_event_eid_exist(self):
        """id已经存在"""
        payload = {"eid":1,"name":"一加4发布会","limit2":2000,"address":"深圳宝体","start_time":"2018-11-01 08:00:00"}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result["status"], 10022)
        self.assertEqual(self.result["message"], "event id already exists")

    def test_add_event_name_exists(self):
        """名称已经存在"""
        payload = {"eid": 88, "name": "红米Pro发布会", "limit2": 2000, "address": "深圳宝体", "start_time": "2018-11-01 08:00:00"}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result["status"], 10023)
        self.assertEqual(self.result["message"], "event name already exists")

    def test_add_event_data_type_error(self):
        """日期格式错误"""
        payload = {"eid": 102, "name": "一加4发布会", "limit2": 2000, "address": "深圳宝体", "start_time": "2018"}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result["status"], 10024)


    def test_add_event_success(self):
        """添加成功"""
        payload = {"eid": 88, "name": "孙小二发布会", "limit2": 2000, "address": "深圳宝体", "start_time": "2018-11-01 08:00:00"}
        print("11111111")
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        print(self.result)
        self.assertEqual(self.result["status"], 200)


if __name__ == '__main__':
    test_data.init_data() # 初始化接口测试数据
    unittest.main()

