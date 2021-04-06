# -*- coding: UTF-8 -*-
import os
import re
import optparse

def test_ffuf(ffuf_path, zoomeye_txt, ffuf_dict_path):
    with open(zoomeye_txt, "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            url = line + "/FUZZ"
            cmd = "{} -w {} -u {} -ac -mc 200,302 -maxtime 120".format(ffuf_path, ffuf_dict_path, url)
            result = os.popen(cmd)
            result = result.buffer.read().decode(encoding='utf-8')           #os.popen输出编码转换
            ffuf2txt(result, line, zoomeye_txt)

def ffuf2txt(result, line, zoomeye_txt):
    result = result.strip("\n")     #去掉换行符
    url_list = result.split("]")
    with open(zoomeye_txt, "a", encoding='utf-8') as f:
        for url in url_list:
            if re.search(".*\[Status:", url):      #排除最后一行
                url = url.split()[0].strip()
                if "[Status" in url:       #部分目录可能为空白
                    continue
                else:
                    url = "\n" + line + "/" + url
                    print(url)
                    f.write(url)

def main(ffuf_path, ffuf_dict_path, zoomeye_http_result):
    test_ffuf(ffuf_path, zoomeye_http_result, ffuf_dict_path)

if __name__ == '__main__':
    main()
