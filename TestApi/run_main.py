# coding:utf-8
import os
import unittest
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db_fixture import test_data
# from  common.logger import Log
# import HTMLTestRunner
import HTMLTestRunnerCN_test
import logging

# 当前脚本所在文件真实路径
cur_path = os.path.dirname(os.path.realpath(__file__))


def add_case(caseName="case",rule="test_*.py"):
    """第一步：加载所有测试用例"""
    case_path = os.path.join(cur_path,caseName) # 用例文件夹
    # 文件夹不存在就创建一个文件夹
    if not os.path.exists(case_path):os.mkdir(case_path)
    # print("test case path:%s"%case_path)
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(case_path,pattern=rule,top_level_dir=None)
    print(discover)
    return discover

def run_case(all_case,reportName="report"):
    """第二步：执行所有的用例，并把结果写入到html测试报告中"""
    now = time.strftime("%Y_%m_%d_%H_%M_%S")
    report_path = os.path.join(cur_path,reportName)
    if not os.path.exists(report_path):os.mkdir(report_path)
    report_abspath = os.path.join(report_path,now+"result.html")
    print("report path:%s"%report_abspath)

    fp = open(report_abspath,"wb")
    runner = HTMLTestRunnerCN_test.HTMLTestRunner(stream=fp,title="自动化接口测试报告，测试结果如下：",
                                           description="用例执行情况")
    # 调用add_case函数
    runner.run(all_case)
    fp.close()


def get_report_file(report_path):
    """第三步：获取最新的测试报告"""
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn:os.path.getmtime(os.path.join(report_path,fn)))
    print(u"最新测试生成的报告："+lists[-1])
    # 找到生成最新的报告文件
    report_file = os.path.join(report_path,lists[-1])
    return report_file

def send_mail(sender,psw,receiver,smtpserver,report_file,port):
    """第四步：发送最新的测试报告内容"""
    with open(report_file,"rb") as f:
        mail_body = f.read()

    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body,_subtype="html",_charset="utf-8")
    msg["Subject"] = "自动化测试报告"
    msg["from"] = sender
    msg["to"] = receiver
    msg.attach(body)

    # 添加附件
    att = MIMEText(open(report_file,"rb").read(),"base64","utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = "attachment;filename = 'report.html'"
    msg.attach(att)
    try:
        smtp = smtplib.SMTP_SSL(smtpserver,port)
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver,port)

    # 用户名密码
    smtp.login(sender,psw)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()
    print("test report email has send out")

if __name__ == '__main__':

    test_data.init_data() # 初始化接口测试数据

    all_case = add_case() # 加载用例
    run_case(all_case)  # 执行用例
    log = logging.getLogger("sss")
    log.warning("提醒")


    report_path = os.path.join(cur_path,"report")
    report_file = get_report_file(report_path)

    # 邮箱配置，邮箱信息获取
    from config import readConfig
    sender = readConfig.sender
    psw = readConfig.psw
    smtp_server = readConfig.smtp_server
    port = readConfig.port
    receiver = readConfig.receiver
    send_mail(sender,psw,receiver,smtp_server,report_file,port) # 调用发送邮件方法
