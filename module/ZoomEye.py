#coding:utf-8
from openpyxl import Workbook
import time
import requests
import json
import optparse
import re
import socket
from urllib.parse import quote
from requests.adapters import HTTPAdapter

result_list = []

def search_zoomeye(dork, page, apikey):
    dork = quote(dork, 'utf-8')
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    burp0_url = "https://api.zoomeye.org/host/search?query={}&page={}".format(dork, page)
    burp0_headers = {"API-KEY": apikey}
    print(burp0_url)
    result = s.get(burp0_url, headers=burp0_headers, timeout=10)
    if result.status_code == 200:
        total = json.loads(result.text)["total"]
        matches = json.loads(result.text)["matches"]
        if total != 0 and matches == []:          #key余额已用完
            return None
        for each_match in matches:
            IP = each_match["ip"]
            portinfo = each_match["portinfo"]
            port = portinfo["port"]
            service = portinfo["service"]
            if "http" in service:
                service = "http"
            elif "https" in service:
                service = "https"
            try:
                title = str(portinfo["title"])
            except:
                title = ""
            url = "{}://{}:{}".format(service, IP, port)
            test_telnet_result = test_socket(IP, port)      #socket连接测试端口通不通
            if test_telnet_result == 1:
                result_list.append([url, service, title])
                print("[+]", url, title.encode("utf-8", "ignore"), "Open")
            else:
                print("[-]", url, title.encode("utf-8", "ignore"), "Close")
                continue
            print(url, title.encode("utf-8", "ignore"))
        return total

    else:           #非200响应码返回错误信息
        print(result.status_code, result.text)


def toexcel(result_list):
    wb = Workbook()
    ws = wb.active
    head = ["url", "service", "title"]
    ws.append(head)
    for list in result_list:
        ws.append(list)
    wb.save('Zfresult\\zoomeye_result.xlsx')

def totxt(result_list):
    with open("zoomeye_http_result.txt", "w", encoding='utf-8') as f:
        for line in result_list:
            if "http" in line[1]:
                f.write(line[0] + "\n")
    f.close()

def test_socket(IP, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(5)
    try:
        sk.connect((IP, port))
        return 1
    except Exception:
        return 0
    sk.close()

def get_apikey():
    apikey_list = []
    with open("APIkey.txt", "r") as f:          #读取关键字
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            burp0_url = "https://api.zoomeye.org/resources-info"
            burp0_headers = {"API-KEY": line}
            result = requests.get(burp0_url, headers=burp0_headers)
            search = json.loads(result.text)["resources"]["search"]
            if search != 0:
                apikey_list.append(line)
            else:
                continue
    return apikey_list

def main(Zoomeye_file_path, add_pram):
    try:
        apikey_list = get_apikey()
        apikey_len = len(apikey_list)
        apikey_index = 0
        with open(Zoomeye_file_path, "r",encoding='utf-8') as f:          #读取关键字
            for line in f.readlines():
                line = line.strip('\n').strip()  # 去掉列表中每一个元素的换行符
                if line == "":        # 有空行会返回500导致报错
                    continue
                else:
                    line = line + " " + add_pram
                if apikey_list == []:
                    print("APIKey一滴也没有了")
                    break
                total = search_zoomeye(line, 1, apikey_list[apikey_index])       #获取第一页数据，并获取total
                if total == None:                    #该key余额已用完
                    apikey_index += 1                #切换到下一个key
                    if apikey_len == apikey_index:    #所有key余额已用完
                        print("APIKey一滴也没有了")
                        break
                    else:
                        total = search_zoomeye(line, 1, apikey_list[apikey_index])          #使用下一个key
                if total <= 20:                 #不用翻页
                    continue
                else:                            #通过total判断是否需要翻页
                    page_num = total//20 + 1      #计算翻页的页数
                    print("[+]Zoomeye总共页数:" + str(page_num))
                    for page in range(2, page_num + 1):
                        print("[+]Zoomeye目前页数:" + str(page))
                        total = search_zoomeye(line, page, apikey_list[apikey_index])
                        if total == None:          #该key余额已用完
                            apikey_index += 1           #切换到下一个key
                            if apikey_len == apikey_index:  #所有key余额已用完
                                print("APIKey一滴也没有了")
                                break
                            else:
                                search_zoomeye(line, page, apikey_list[apikey_index])          #使用下一个key
                print(result_list)
    except Exception as e:
        print(str(e))

    totxt(result_list)
    toexcel(result_list)

if __name__ == '__main__':
    main()