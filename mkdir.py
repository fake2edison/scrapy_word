# -*- coding:utf-8 -*-

import xlrd
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(1000000)


def getFirst(list1, list2):
    for i in range(0, list1.__len__()):
        if str(list1[i]).split('.')[1] == '0':
            print list1[i]


def getFater(list1, list2, indextemp):
    pathTemp = ""
    if str(list1[indextemp]).split('.')[-1] == '0' or str(list1[indextemp]).isdigit():
        # 如果最后一个为0 则应该作为父目录
        # 有情况为 1.0   1.2.0
        # pathTemp = list2[indextemp]  # 这是作为最开始的
        # 当不是父节点的时候 需要找到最邻近的一项作为前缀
        # list1 list2 是已经提供的列表，不需要改动
        # indextemp 是当前节点的下标,此时需要定位到父节点的下标
        # if str(list1[indextemp]).split('.').__len__() == 2:
        # print "if" + str(list1[indextemp])
        pathTemp = list2[indextemp]
        # else:
        #     print list2[indextemp]
        #     lastIndex = find_last(str(list1[indextemp]), '.')
        #     strTemp = str(list1[indextemp])[:lastIndex] + '.0'
        #     index = 0
        #     for i in range(0, list1.__len__()):
        #         if strTemp == str(list1[i]):
        #             index = i
        #             break
        #     pathTemp = getFater(list1, list2, index) + '\\' + pathTemp
    else:
        lastIndex = find_last(str(list1[indextemp]), '.')
        # str(indextemp)[:lastIndex] 为最后一个小数点以前的数
        strTemp = str(list1[indextemp])[:lastIndex]
        index = 0
        pathTemp = list2[indextemp]
        # print "pathTemp" + list1[indextemp]
        # print "strTemp" + strTemp
        if nohasSpitl(strTemp):
            #     说明为最上级的
            for i in range(0, list1.__len__() - 1):
                if strTemp == str(list1[i])[0:strTemp.__len__()]:
                    index = i
                    break
        else:
            for i in range(0, list1.__len__()):
                if strTemp == str(list1[i]) or strTemp == list1[i]:
                    # pathTemp = list2[i] + '\\' + list2[indextemp]
                    # break
                    index = i
                    break
        # print "else" + str(list1[index])
        pathTemp = getFater(list1, list2, index) + '\\' + pathTemp
    return pathTemp


def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


def nohasSpitl(s):
    s_spi = s.replace(".", "")
    if s == s_spi:
        return True
    else:
        return False


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        # print path + 'success'
        return True
    else:
        # print path + ' exist'
        return False


def notCom(s):
    if str(s).isdigit():
        return True
    elif str(s).replace(" ", "") == "":
        return False
    elif str(s).replace(".", "").isdigit():
        return True
    else:
        return False


def delZero(s):
    if str(s)[0] == '0':
        s = str(s)[1:s.__len__()]
    return str(s)


if __name__ == '__main__':
    worksheet = xlrd.open_workbook('1.xlsx')
    sheet = worksheet.sheet_by_name('Sheet1')
    col1 = sheet.col_values(0)
    col2 = sheet.col_values(1)
    col1_1 = []
    col2_1 = []
    for i in range(0, col1.__len__() - 1):
        # print str(col1[i]) + str(col2[i])
        if notCom(col1[i]):
            col1_1.append(delZero(col1[i]))
            col2_1.append(col2[i])

    # for t in range(0, col1_1.__len__()):
    #     print str(col1_1[t]) + str(col2_1[t])
    # print (col1)
    # for i in col2:
    #     print i.encode('utf-8')
    # for i in range(0, col1.__len__()):
    #     print (str(col1[i]) + "   " + col2[i].encode("utf8"))
    # getFirst(col1, col2)
    for i in range(0, col1_1.__len__()):
        # print col1_1[i]
        pathTemp = getFater(col1_1, col2_1, i)
        # print pathTemp
        mkdir(pathTemp)