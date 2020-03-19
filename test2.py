#导入需要使用到的模块
import urllib
import urllib.request
import re
import os
import pandas as pd
import pymysql
import socket
#爬虫抓取网页函数
def getHtml(url):
    html=""
    try:
        response = urllib.request.urlopen(url,timeout=20)
        try:
            html = response.read()
            html = html.decode("gbk", "ignore")
        except:
            print (读取失败)
        response.close()
        del response
        return html
    except urllib.error.URLError as e:
        print(e.reason)
    except socket.timeout as e:
        print("-----socket timout:", url)
    except UnicodeDecodeError as e:
        print('-----UnicodeDecodeError url:', url)
    finally:
        return html

        #抓取网页股票代码函数
def getStackCode(html):
    # s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    s=r'<a href="/stock/lhb/yyb/(.*?).html">(.*?)</a>'

    pat = re.compile(s)
    code = pat.findall(html)
    return code
with open('stockid.txt','r') as f:
    content = f.read().splitlines()
    for line in content:
         print (line)
         for m in range(1, 9):
             for d in range(1, 32):
                 if m == 2 and d > 28:
                     continue
                 if m == 4 or m == 6 :
                     if d > 30:
                        continue
                 if d < 10:
                     d = '0' + str(d)
                 Url = 'http://data.eastmoney.com/stock/lhb,2019-0' + str(m) + '-' + str(d) + ','+line+'.html'  # 龙虎榜
                 filepath = 'H:\\Share\\Stock\\'  # 定义数据文件保存路径
                 # 实施抓取
                 codelist = getStackCode(getHtml(Url))

                 name = 'root'
                 password = 'wasd5123'  # 替换为自己的账户名和密码
                 # 建立本地数据库连接(需要先开启数据库服务)
                 db = pymysql.connect('localhost', name, password, charset='gbk')
                 cursor = db.cursor()
                 sqlSentence2 = "use lhb;"
                 cursor.execute(sqlSentence2)
                 try:
                     sqlSentence3 = "create table stock_"+ line + " (日期 date, 数据 VARCHAR(89), PRIMARY KEY (日期))"
                     cursor.execute(sqlSentence3)
                 except:
                     print('已存在')

                 data = '2019/0' + str(m) + '/' + str(d)
                 print(data)

                 codeall = ""

                 for code in codelist:
                     codeall = codeall + code[0] + ','
                 if codeall == "":
                     print("数据为空")
                 else:
                     print(codeall)
                     codeall = codeall[:89]

                     sqlSentence4 = "replace into stock_" + line + "(日期,数据) values ('%s','%s')" % (data, codeall)
                     cursor.execute(sqlSentence4)
                     cursor.close()
                     db.commit()
                     db.close()

