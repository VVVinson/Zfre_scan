import module.XRaEh
import module.ZoomEye
import os
import module.ffuf
import optparse
import re

def get_config(zfre_scan_config):
    with open(zfre_scan_config, "r", encoding='utf-8') as f:
        for line in f.readlines():
            if re.search("Zoomeye_file_path = (.*)", line):
                Zoomeye_file_path = line.split("=")[1].strip()
            if re.search("ffuf_path = (.*)", line):
                ffuf_path = line.split("=")[1].strip()
            if re.search("ffuf_dict_path = (.*)", line):
                ffuf_dict_path = line.split("=")[1].strip()
            if re.search("Ehole_path = (.*)", line):
                Ehole_path = line.split("=")[1].strip()
            if re.search("rad_path = (.*)", line):
                rad_path = line.split("=")[1].strip()
            if re.search("xray_path = (.*)", line):
                xray_path = line.split("=")[1].strip()
            if re.search("zoomeye_http_result = (.*)", line):
                zoomeye_http_result = line.split("=")[1].strip()
    return Zoomeye_file_path, ffuf_path, ffuf_dict_path, Ehole_path, rad_path, xray_path, zoomeye_http_result

def main():
    usage = "python %prog -m/M zfre -c/C <zfre_scan.config path>"  # 用于显示帮助信息
    parser = optparse.OptionParser(usage)  # 创建对象实例
    parser.add_option('-M', '-m', dest='module', type='string', help='python module(z,f,re)', default='zfre')  ## -p/-P 都可以
    parser.add_option('-C', '-c', dest='config', type='string', help='zfre_scan.config path', default='zfre_scan.config')  ## -p/-P 都可以
    (options, args) = parser.parse_args()
    Zoomeye_file_path, ffuf_path, ffuf_dict_path, Ehole_path, rad_path, xray_path , zoomeye_http_result= get_config(options.config)
    print(options.module)

    if re.search("z", options.module, re.IGNORECASE):
        print("----------Start ZoomEye.py-----------")
        module.ZoomEye.main(Zoomeye_file_path)
    if re.search("f", options.module, re.IGNORECASE):
        print("-----------Start ffuf.py-------------")
        module.ffuf.main(ffuf_path, ffuf_dict_path, zoomeye_http_result)
    if re.search("re", options.module, re.IGNORECASE):
        print("-----------Start XRaEh.py------------")
        module.XRaEh.main(Ehole_path, rad_path, xray_path, zoomeye_http_result)

if __name__ == '__main__':
    main()