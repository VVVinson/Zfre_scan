# Zfre_scan
HVV信息收集，优秀开源工具的整合，通过Zoomeye+ffuf+EHole+Xray+Rad进行自动化信息收集与结果输出

分为三个模块：  
1、Zoomeye.py：调用zoomeye接口获取数据  
2、ffuf.py：调用ffuf对url列表进行目录扫描  
3、XraEh.py：调用xray与rad对url列表进行爬虫与被动扫描  


 - Input：Zoomeye搜索的关键字
 - Output：ffuf目录扫描结果、EHole指纹识别结果、Xray+Rad扫描结果
 
**本项目所有内容仅作为安全研究和授权测试使用, 相关人员对因误用和滥用该项目造成的一切损害概不负责**

## 运行环境
语言：python3  

操作系统：目前只试过windows上使用  

Python模块：openpyxl    

 `pip install openpyxl`
 

## 配置：
### 1、下载各个模块使用到的开源工具：

Zoomeye获取IP、端口、协议（无需下载，需要注册获取APIkey）:[https://www.zoomeye.org/](https://www.zoomeye.org/)

ffuf目录扫描（目录字典也需要准备）：[https://github.com/ffuf/ffuf](https://github.com/ffuf/ffuf)

EHole指纹识别、title识别：[https://github.com/EdgeSecurityTeam/EHole](https://github.com/EdgeSecurityTeam/EHole)

Xray被动扫描：[https://github.com/chaitin/xray](https://github.com/chaitin/xray)

Rad爬虫：[https://github.com/chaitin/rad](https://github.com/chaitin/rad)

### 2、zfre_scan.config配置文件写入信息：

```
Ehole_path = Ehole绝对路径 
ffuf_path = ffuf绝对路径 
ffuf_dict_path = ffuf目录字典绝对路径 
rad_path = rad绝对路径 
xray_path = xray绝对路径 
Zoomeye_file_path = zoomeye读取的关键字或者C段文件路径 
zoomeye_http_result = ffuf、rad、xray、Ehole读取的url文件路径（文件里需要带上http或者https协议）
```

## 使用：
### 1、多模块调用：

```
1、Zoomeye+ffuf+EHole+Xray+Rad：  python zfre_scan.py -m zfre
2、Zoomeye+EHole+Xray+Rad：       python zfre_scan.py -m zre
3、ffuf+EHole+Xray+Rad：          python zfre_scan.py -m fre
4、Zoomeye+ffuf：                 python zfre_scan.py -m zf

输入：├── dork.txt                #zoomeye读取的关键字或者C段文件路径，需要配置到zfre_scan.config里
输出：
├── Zfresult                     #结果输出目录
│   ├── xray_result.html         #xray扫描结果
│   ├── EHole_result.xlsx        #EHole指纹识别结果
│   └── zoomeye_result.xlsx      #zoomeye输出结果，主要看非http协议
└── zoomeye_http_result.txt      #zoomeye.py执行输出的http协议url（暂时无法修改输出路径与文件名）；ffuf.py的输入；ffuf.py执行后会在这里新增扫描到的url
```
### 2、单模块调用：
```
1、Zoomeye：                     python zfre_scan.py -m z
输入：├── dork.txt               #zoomeye读取的关键字或者C段文件路径，需要配置到zfre_scan.config里
输出：
├── Zfresult #结果输出目录
│   └── zoomeye_result.xlsx      #zoomeye输出结果，主要看非http协议
└── zoomeye_http_result.txt      #zoomeye.py执行输出的http协议url（暂时无法修改输出路径与文件名）

2、EHole+Xray+Rad：               python zfre_scan.py -m re
输入：├── zoomeye_http_result.txt #url，每个url直接换行，需要带上http://或https://
输出：
├── Zfresult                     #结果输出目录
│   ├── xray_result.html         #xray扫描结果
│   └── EHole_result.xlsx        #EHole指纹识别结果
└────────────────────────

3、ffuf：                         python zfre_scan.py -m f
输入：├── zoomeye_http_result.txt #url，每个url直接换行，需要带上http://或https://
输出：
└── zoomeye_http_result.txt       #ffuf.py模块执行后会在后面新增扫描到的url
```
## 注：
- 每次使用前需要自行重命名或者移走Zfresult目录下的文件，否则会覆盖原有结果，或者Xray无法监听
- Xray目前需要手动关掉监听进程
