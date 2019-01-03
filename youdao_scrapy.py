# -*- coding:utf-8 -*-
from urllib import request
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
import sys


def trim(s):
    if len(s) == 0:
        return s
    elif s[0] == ' ' or s[0] == '\n':
        return (trim(s[1:]))
    elif s[-1] == ' ' or s[-1] == '\n':
        return (trim(s[:-1]))
    return s


class Spider_Vedio:
    def load_page(self, word):
        word = quote(word, 'utf-8')
        url = "http://www.youdao.com/w/" + word + "/#keyfrom=dict2.top"
        # print(url)
        user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"
        headers = {'User-Agent': user_agent}
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        html = str(response.read(), 'UTF-8', 'ignore')
        return html

    def do_work(self, word):
        html = self.load_page(self, word)
        html = BeautifulSoup(html, 'html.parser')
        temp = ""
        # print(html)
        try:
            s = trim(re.sub(r'[^\x00-\x7f]', ' ', html.select('a.search-js')[0].text))
            if s != '':
                # print(s)
                if temp != '':
                    temp = s + '+' + temp
                else:
                    temp = s
            # print(trim(re.sub(r'[^\x00-\x7f]', ' ', html.select('a.search-js')[0].text)))
        except:
            pass
        try:
            s = trim(re.sub(r'[^\x00-\x7f]', ' ', html.select('p.wordGroup')[0].text))
            if s != '':
                # print(s)
                if temp != '':
                    temp = s + '+' + temp
                else:
                    temp = s
            # print(trim(re.sub(r'[^\x00-\x7f]', ' ', html.select('p.wordGroup')[0].text)))
        except:
            pass
        try:
            s = trim(re.sub(r'[^\x00-\x7f]', ' ', html.select('div#fanyiToggle')[0].select('p')[1].text))
            if s != '':
                # print(s)
                if temp != '':
                    temp = s + '+' + temp
                else:
                    temp = s
            # print(trim(re.sub(r'[^\x00-\x7f]', ' ', html.select('div#fanyiToggle')[0].select('p')[1].text)))
        except:
            pass
        try:
            s = trim(re.sub(r'[^\x00-\x7f]', ' ', html.select('div.title')[0].select('span')[0].text))
            if s != '':
                # print(s)
                if temp != '':
                    temp = s + '+' + temp
                else:
                    temp = s
            # print(trim(re.sub(r'[^\x00-\x7f]', ' ', html.select('div.title')[0].select('span')[0].text)))
            # res_tr = r'src="(.*?)" id'
            # m_tr = re.findall(res_tr, html, re.S | re.M)
            # date = last_date.replace('/', '')
            # for m in m_tr:
            #     print(m)
        except:
            pass
        print(temp)


if __name__ == '__main__':

    file = open('1.txt', 'r', encoding="utf8")

    context = file.readlines()

    spider_vedio = Spider_Vedio

    for i in context:
        print(i, end='')
        spider_vedio.do_work(spider_vedio, i)
        print("\n")
    # spider_vedio.do_work(spider_vedio, "阿里巴巴集团控股有限公司")
    file.close()
