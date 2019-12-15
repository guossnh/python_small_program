#-*- coding : utf-8 -*-

import xlwt,xlrd,csv,os
import  pandas as pd


desktop_link = "C:\\Users\\Administrator\\Desktop\\"
path =  "C:\\Users\\Administrator\\OneDrive\\save\\save\\"



def readexcle():
    book = xlrd.open_workbook("C:\\Users\\Administrator\\OneDrive\\save\\save\\maideduo\\2019-08-01-2019-09-30已发货查询结果3068.xlsx")
    booksheet = book.sheet_by_index(0)
    rows=booksheet.get_rows()
    wocao = 0
    for row in rows:
        if("乳" in row[7].value or "宫" in row[7].value or "女" in row[7].value or "脱皮" in row[7].value or "痛经" in row[7].value):
            try:
                #writecsv(row[4].value,row[5].value,row[6].value)
                wocao+=1
            except:
                pass
        elif("G-" in row[16].value or "G" in row[16].value):
            try:
                writecsv(row[4].value,row[5].value,row[6].value)
                wocao+=1
            except:
                pass

#写入csv
def do_csv():
    with open("C:\\Users\\Administrator\\OneDrive\\save\\save\\枕头\\ExportOrderList201912101536.csv","rb") as file:
        #re = csv.reader(file)
        re = file.readlines()
        content =0
        content2 =0
        content3 =0
        content4 =0
        print(str(re[0],encoding="gbk"))
        for x in re:
            content+=1
            wocao = ""
            try:
                wocao =  str(x,encoding="gbk")
                content2+=1
                wocao = wocao.split(",")
                wocao2 = wocao[19]
                wocao3 = wocao[23]
                if ("乳" in wocao2 or "宫" in wocao2 or "女" in wocao2 or "脱皮" in wocao2 or "痛经" in wocao2 or "洗" in wocao2):
                    content3+=1
                    #username = wocao[12].replace("\"","")
                    #userphone = wocao[16].replace("\"","").replace("\'","")
                    #useradd =wocao[13].replace("\"","")
                    #writecsv(username,userphone,useradd)
                elif("G-" in wocao3):
                    content4+=1
                    username = wocao[12].replace("\"","")
                    userphone = wocao[16].replace("\"","").replace("\'","")
                    useradd =wocao[13].replace("\"","")
                    writecsv(username,userphone,useradd)
            except:
                pass

            #  12  13  16

        print("总共处理了"+str(content)+"条数据")
        print("以gbk方式处理了"+str(content2)+"条数据")
        print("选出了"+str(content3)+"条数据")
        print("选出了"+str(content4)+"条备用数据")

        '''
        for x in re:
            try:
                content2 +=1
                if ("乳" in x[19] or "宫" in x[19] or "女" in x[19] or "脱皮" in x[19] or "痛经" in x[19]or "洗" in x[19]):
                    content+=1
            except:
                pass
        '''



def findfile():
    file_all = []
    file_csv = []
    for root, dirs, files in os.walk(path):
        file_all = file_all+ files
    for x in file_all:
        if("OrderList" in  x):
            file_csv.append(x)
    return file_csv

def writecsv(name,phone,address):
    with open(""+desktop_link+"result7.csv","a+",newline = '') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow([name,phone,address])

#查询重复量
def findother():
    data = pd.read_csv("C:\\Users\\Administrator\\Desktop\\result9.csv",encoding="utf8")
    #data2 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\result2.csv",encoding="utf8")
    #data2 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\all.csv", encoding="gbk",delimiter="\t")
    #df = pd.merge(data3, data2, how='left', on='phone')
    #data.to_csv('C:\\Users\\Administrator\\Desktop\\result3.csv',index=False)
    #df = pd.concat([data1, data2],axis=0) 
    #print(data.duplicated(subset = ['phone'],keep="last"))
    newdata  = data.drop_duplicates(['phone'],keep="last")
    #new1  = data.drop(data.index[179242:])
    #new1 = new1.drop(['n1'],axis=1)
    #new2 = data.drop(data.index[0:179241])
    #new2 = data2.drop(['u1'],axis=1)
    #new1.to_csv('C:\\Users\\Administrator\\Desktop\\result1.csv',index=False)
    #new2.to_csv('C:\\Users\\Administrator\\Desktop\\result2.csvd',index=False)
    newdata.to_csv('C:\\Users\\Administrator\\Desktop\\result8.csv',index=False)

findother()
