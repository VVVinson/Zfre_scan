# -*- coding: utf-8 -*-
import os
import time
from multiprocessing import Process
from openpyxl import Workbook
import optparse
import re

def toexcel(result_list):
    wb = Workbook()
    ws = wb.active
    head = ["url", "指纹", "APP", "状态码", "size", "title"]
    ws.append(head)
    for list in result_list:
        ws.append(list)
    wb.save('Zfresult\\EHole_result.xlsx')

def rad(zoomeye_http_result, rad_path):
    with open(zoomeye_http_result, "r",encoding='utf-8') as f:          #读取关键字
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            os.system("{} -t {} -http-proxy 127.0.0.1:7770".format(rad_path, line))
    print("----------------Rad爬虫结束----------------")

def xray(xray_path):
    cmd = "{} webscan --listen 127.0.0.1:7770 --html-output Zfresult\\xray_result.html".format(xray_path)
    os.system(cmd)
    print(cmd)

def Ehole(zoomeye_http_result, Ehole_path):
    Ehole_path = Ehole_path.split("\\", -1)
    print("\\".join(Ehole_path[:-1]))
    cmd = "cd {} & {} -l {}".format("\\".join(Ehole_path[:-1]), Ehole_path[-1], zoomeye_http_result)
    Ehold_result = os.popen(cmd)             # 这个地方不能合并一行写，会出错说 read of closed file
    Ehold_result = Ehold_result.buffer.read().decode(encoding='utf8')
    new_list = []
    Ehold_result_list = Ehold_result.split("[")
    for each_Ehold_result in Ehold_result_list:
        new_list.append(each_Ehold_result.split("|"))
        if "重点资产：" in each_Ehold_result:
            new_list.append(["重点资产："])
    toexcel(new_list)

def main(Ehole_path, rad_path, xray_path, zoomeye_http_result):
    zoomeye_http_result = os.getcwd() + "\\" + zoomeye_http_result
    p3 = Process(target=Ehole, kwargs={'zoomeye_http_result': zoomeye_http_result, 'Ehole_path': Ehole_path})
    p1 = Process(target=xray, kwargs={'xray_path': xray_path})
    time.sleep(30)
    p2 = Process(target=rad, kwargs={'zoomeye_http_result': zoomeye_http_result, 'rad_path': rad_path})
    p1.start()
    p3.start()
    p2.start()

if __name__ == '__main__':
    main()