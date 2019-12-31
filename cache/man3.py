#-*- coding : utf-8 -*-

import xlwt,xlrd,csv,os
import  pandas as pd


desktop_link = "C:\\Users\\Administrator\\Desktop\\"

path_csv =  "D:\\chache\\tb\\"
path_xlsx =  "D:\\chache\\pd\\"


def readexcle(filname):
    book = xlrd.open_workbook(filname)
    booksheet = book.sheet_by_index(0)
    rows=booksheet.get_rows()
    for row in rows:
        if("乳" in row[7].value or "宫" in row[7].value or "女" in row[7].value or "脱皮" in row[7].value or "痛经" in row[7].value or "腱鞘" in row[7].value ):
            try:
                write_nv_csv(row[4].value,row[5].value,row[6].value)
            except:
                pass
        elif("G-" in row[16].value or "g-" in row[16].value or"V-" in row[16].value or "v-" in row[16].value ):
            try:
                write_nv_csv(row[4].value,row[5].value,row[6].value)
            except:
                pass
        else:
            try:
                write_other_csv(row[4].value,row[5].value,row[6].value)
            except:
                pass

#写入csv
def do_csv(filename):
    with open(filename,"rb") as file:
        #re = csv.reader(file)
        re = file.readlines()
        content =0
        content2 =0
        content3 =0
        content4 =0
        for x in re:
            content+=1
            wocao = ""
            try:
                wocao =  str(x,encoding="gbk")
                content2+=1
                wocao = wocao.split(",")
                wocao2 = wocao[19]
                wocao3 = wocao[23]
                username = wocao[12].replace("\"","")
                userphone = wocao[16].replace("\"","").replace("\'","")
                useradd =wocao[13].replace("\"","")
                if ("乳" in wocao2 or "宫" in wocao2 or "女" in wocao2 or "脱皮" in wocao2 or "痛经" in wocao2 or "洗" in wocao2 or "腱鞘" in wocao2):
                    content3+=1
                    write_nv_csv(username,userphone,useradd)
                elif("G-" in wocao3 or "V-" in wocao3 or "g-" in wocao3 or "v-" in wocao3):
                    content4+=1
                    write_nv_csv(username,userphone,useradd)
                else:
                    write_other_csv(username,userphone,useradd)
            except:
                pass

            #  12  13  16

        #print("总共处理了"+str(content)+"条数据")
        #print("以gbk方式处理了"+str(content2)+"条数据")
        #print("选出了"+str(content3)+"条数据")
        #print("选出了"+str(content4)+"条备用数据")

def findfilecsv():
    for _, _, files in os.walk(path_csv):
        for x in files:
            print(path_csv+x)
            do_csv(path_csv+x)
    for _, _, files in os.walk(path_xlsx):
        for x in files:
            print(path_xlsx+x)
            readexcle(path_xlsx+x)


def write_nv_csv(name,phone,address):
    with open(""+desktop_link+"nv.csv","a+",newline = '') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow([name,phone,address])

def write_other_csv(name,phone,address):
    with open(""+desktop_link+"other.csv","a+",newline = '') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow([name,phone,address])
#查询重复量

def findother():
    data = pd.read_csv("C:\\Users\\Administrator\\Desktop\\other.csv",encoding="gbk")
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
    newdata.to_csv('C:\\Users\\Administrator\\Desktop\\other_rel.csv',index=False)

findother()