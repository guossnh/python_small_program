#-*- coding : utf-8 -*-
#帮助谢艳丽筛选拼多多导出表格两个条件的ID
import xlwt,os,xlrd,re,csv
from datetime import datetime

#下边是设置的一些变量
usedID = []#这个用来存放有用的ID
xlsxfile = 'C:\\xlsx\\'
xlsxonefile = 'C:\\xlsx\\'
numall = 0
numDateSame = 0
numDateTen = 0
numright = 0

#用来读取xlsx文件获取里边的信息
def readxlsx(): 
    pass
#生成老谢需要的文件相同的名字
def maketxt():
    global xlsxonefile,numall,numDateSame,numDateTen,numright,usedID,xlsxfile
    workbook = xlrd.open_workbook(xlsxonefile)
    booksheet = workbook.sheet_by_index(0)
    for a in range(1,booksheet.nrows):
        if(re.match(r'\d{6}-\d+',booksheet.cell_value(a,0))):
            numall = numall + 1
            #print(booksheet.cell_value(a,0))
            #print(xlrd.xldate_as_tuple(booksheet.cell_value(a,1),0))
            #print(xlrd.xldate_as_datetime(booksheet.cell_value(a,1),0))
            pddId = booksheet.cell_value(a,0)
            timelist = xlrd.xldate_as_tuple(booksheet.cell_value(a,1),0)
            timelist2 =datetime.strptime((str(xlrd.xldate_as_datetime(booksheet.cell_value(a,1),0))[0:10]), '%Y-%m-%d')
            #print("~~~~~~~~~~~~~~~~~~~~~")
            #print(timelist[1],"+++",timelist[2])
            #print(int(pddId[2:4]),"+++",int(pddId[4:6]))
            pddIdTime = datetime.strptime('20'+pddId[0:2]+'-'+pddId[2:4]+'-'+pddId[4:6], '%Y-%m-%d')

            if((timelist[1]==int(pddId[2:4]))&(timelist[2]==int(pddId[4:6]))):
                #print('我是日期一样',booksheet.cell_value(a,0))
                numDateSame = numDateSame + 1
                continue
            elif((timelist[3]<10)&((timelist2-pddIdTime).days==1)):
                #print('我是10点日期差一天',booksheet.cell_value(a,0))
                numDateTen = numDateTen + 1
                continue
            else:
                numright = numright + 1
                usedID.append(booksheet.cell_value(a,0))
    with open(xlsxfile+"rightID.txt","a",newline='') as csvfile: 
        for value in usedID:
            csvfile.write(value)
            csvfile.write('\n')


if __name__ == "__main__":
    #读取文件夹找到一个xlsx文件开始处理
    for file in os.listdir(xlsxfile):
        if file.find("xlsx")!=-1:
            xlsxonefile = xlsxonefile + file
            break
    if(len(xlsxonefile)>12):
        print('已经找到文件，稍等~~~')
        maketxt()
        print('已经处理完毕')
        print('总共处理'+str(numall)+'条数据')
        print('时间相同的数据有'+str(numDateSame)+'条')
        print('第二天10点之前的数据有'+str(numDateTen)+'条')
        print('你需要的数据有'+str(numright)+'条，已经生成txt文件放在文件夹里边,不谢')
    else:
        print('脑残！文件夹里边根本没有文件')
