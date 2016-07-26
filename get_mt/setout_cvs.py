#-*- coding : utf-8 -*-
#数据导出成csv


#导包
import sqlite3
import csv




#变量
conn = sqlite3.connect('meituan.db')
headers = ['姓','名','前缀','后缀','家庭电话','家庭电话 2','工作电话','工作电话 2','备注','电子邮件','其他电话','其他电话 2','其他电话 3','其他手机','其他手机 2','qq同步助手','分组']
road = "D:\git\get_meituan\data\meituan1.csv"

#这是用于记录写入的信息条数
rownum = 0

#用于标记文件的数量也用于文件名字
filenum = 1

#这是文件内容
rows = []


#程序
def select_db(rowid):
    global conn
    c = conn.cursor()
    c.execute("select * from  meituandb where rowid = '%s' " % rowid)
    data=c.fetchone()
    if data is None:
        print("这是没有数据")
    elif data[3] == '':
        pass
    else:
        make_csv(data[0],data[3],data[4],data[6])

def make_csv(name,phone1,phone2,add):
    global rownum , rows
    rownum = rownum + 1
    row = ['','','','','','','',]
    row.insert(0,name)
    row.insert(4,phone1)
    row.insert(5,phone2)
    row.insert(8,add)
    rows.append(row)
    #这是判断一个文件有多少条数据的.测试的话先用10条.往后 再加
    if rownum>299:
        print("成功写成一个文档")
        writeFile()
        content()
        rows = []
        rownum = 0

def content():
    global filenum , road
    filenum = filenum + 1
    road = road[:31] + str(filenum) +'.csv'

def writeFile():
    global road
    with open(road,'w',newline='',encoding="utf8") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
    f.close()




def main():
    #select_db()
    num = 1
    while num<69907:
        select_db(num)
        num = num + 1

    #do the last content
    with open("D:\git\get_meituan\data\last.csv",'w',newline='',encoding="utf8") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
    f.close()

    conn.close()


if __name__ == '__main__':
    main()