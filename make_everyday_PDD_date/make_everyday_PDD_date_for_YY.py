#-*- coding : utf-8 -*-
#根据固定文件夹下边整理的全公司的销售数据和直通车数据共同计算出最终结果。

import pandas as pd
import numpy as np
import time,os,datetime,glob,sys,csv,xlrd
import urllib.request

boy_name = ""
product_list =[]
product_file_list =[]
man_URL = "d:\\make_everyday_PDD_date_for_YY\\"
product_link_in_list = []#这个是所有产品信息对象的存储
product_name_and_easy_name_list = []

#根据所有文件整合数据在一块放入对象
def make_all_file():
    #获取桌面的需要统计的所有文件的数据
    def get_file_name_list():
        #now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        return glob.glob(r''+man_URL+'file\\*.csv')
    global product_file_list
    for product_file in get_file_name_list():
        product_file_list.append(pd.read_csv(product_file))
    return pd.concat(product_file_list)

def kaiguan():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False

#直通车花费统计直接通过ID找到花费金额
def get_money_car(productID):
    car_money_file_list=[]
    car_money_pd =[]
    yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    yes_time = yes_time.strftime('%Y%m%d')
    try:
        car_money_file_list = glob.glob(r''+man_URL+'file\\*.xls')
        for x in car_money_file_list:
            car_money_pd.append(pd.read_excel(x))
        resultpd = pd.concat(car_money_pd)
        #print(resultpd['花费(元)'])#print(resultpd['花费(元)'])
        one_resultpd = resultpd[(resultpd['推广计划'].str.find(productID, start=0, end=None)>=0)]
        if(len(one_resultpd)):
            return one_resultpd["花费(元)"].sum()
        else:
            return 0
    except:
        return 0

#读取配置放产品对象进入对象的数组
def read_config_xlsx():
    global man_URL,product_link_in_list,product_name_and_easy_name_list
    #读取文件并且获取组列表
    xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",None)
    #去掉数据表格其他的表格名字加入Class_leader
    for x in xl.keys():
        if(x.find("组")!= -1):
            xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",x)
            xl['产品ID'] = pd.to_numeric(xl['产品ID'], errors='coerce')
            xl = xl.dropna(subset=['产品ID'])
            #xl['产品ID'] = xl['产品ID'].astype(int)
            for row in xl.itertuples():
                #print(getattr(row, '店铺'), getattr(row, '产品简称'))
                product_link_in_list.append(product_link_in(int(getattr(row, '产品ID')),getattr(row, '店铺'),getattr(row, '产品简称'),getattr(row, '姓名'),0,0,0,0,x))
        elif(x.find("数据")!= -1):
            xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",x)
            for row in xl.itertuples():
                product_name_and_easy_name_list.append(product_name_and_easy_name(getattr(row, '产品名称'),getattr(row, '产品简称')))
    return product_link_in_list

def find_product_full_name(easyname):
    global product_name_and_easy_name_list
    for x in product_name_and_easy_name_list:
        if(x.ename==easyname):
            return x.name
    return "没有名字"

#这个是匹配每一个产品简称和全程的类
class product_name_and_easy_name:
    def __init__(self,name,ename):
        self.name = name
        self.ename = ename
#这个是对应每一个产品链接的对象，包括直通车数据，销售额，刷单
class product_link_in:
    def __init__(self,pid,shop,ename,pname,car_money,shell_money,sd_money,wb_money,group):
        self.pid = pid
        self.shop = shop
        self.ename = ename
        self.pname = pname
        self.car_money = car_money
        self.shell_money = shell_money
        self.sd_money = sd_money
        self.wb_money = wb_money
        self.group = group

def writer_file():
    global boy_name
    result_file = make_all_file()
    result_file = result_file.drop_duplicates(['订单号'])
    all_date = result_file[(result_file["售后状态"]=="无售后或售后取消")|(result_file["售后状态"]=="售后处理中")]
    all_date = all_date[(all_date["订单状态"]=="待发货")|(all_date["订单状态"]=="已发货，待签收")|(all_date["订单状态"]=="已签收")|(all_date["订单状态"]=="已发货，待收货")|(all_date["订单状态"]=="已收货")]
    #all_date["商家备注"] = all_date["商家备注"].str.split(";").str[-1]
    all_date["商品id"].astype("str")
    for one_date in read_config_xlsx():
        try:
            all_shell = all_date[(all_date["商品id"]==one_date.pid)]["商家实收金额(元)"].sum()
            wb_make_shell = all_date[(all_date["商品id"]==one_date.pid)&((all_date["商家备注"].str.contains("V-"))| (all_date["商家备注"].str.contains("v-")))]["商家实收金额(元)"].sum()
            sd_make_shell = all_date[(all_date["商品id"]==one_date.pid)&((all_date["商家备注"].str.contains("G-"))|(all_date["商家备注"].str.contains("g-")))]["商家实收金额(元)"].sum()
            one_date.wb_money = round(wb_make_shell,2)
            one_date.sd_money = round(sd_make_shell,2)
            one_date.shell_money = round(all_shell-wb_make_shell-sd_make_shell,2)
            one_date.car_money = get_money_car(str(one_date.pid))
        except:
            pass

    #先要把数组对象转变成为pandas对象方便透视操作
    #先把对象转化为数组数据
    pname = []
    group = []
    shop = []
    pid = []
    ename = []
    shell_money = []
    sd_money = []
    wb_money = []
    car_money = []
    for i in product_link_in_list:
        pname.append(i.pname)
        group.append(i.group)
        shop.append(i.shop)
        pid.append(i.pid)
        ename.append(i.ename)
        shell_money.append(i.shell_money)
        sd_money.append(i.sd_money)
        wb_money.append(i.wb_money)
        car_money.append(i.car_money)
    dit ={"姓名":pname,"组":group,"店名":shop,"ID":pid,"产品简称":ename,"真实销售额":shell_money,"刷单":sd_money,"放单":wb_money,"直通车":car_money}
    df =pd.DataFrame(dit)
    #print(df)

    yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    yes_time = yes_time.strftime('%Y-%m-%d')
    df["日期"] = yes_time
    #输出个人销量文件
    df1 = pd.pivot_table(df,index=['日期','姓名','店名','产品简称','ID'],values=['真实销售额','刷单','放单','直通车'],aggfunc=np.sum).round(2)
    #df1.rename(columns={'pname':'姓名','shop':'店名','ename':'产品简称','shell_money':'真实销售额','sd_money':'刷单','wb_money':'放单','car_money':"直通车"},inplace = True)
    #print(df1)
    #去除是0的行
    #df1=df1[(df1["真实销售额"]!=0.0)|(df1["刷单"]!=0.0)|(df1["放单"]!=0.0)|(df1["直通车"]!=0.0)]
    #df1["日期"] = yes_time
    print(df1)
    df1 = df1[['真实销售额','刷单','放单','直通车']]
    df1.to_csv(""+man_URL+yes_time+"每个人销量文件.csv",sep=',')

    with open(""+man_URL+"result.csv","w",newline = '') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["姓名","组","店","产品ID","产品全称","销量","刷单","放单","直通车"])
        for i in product_link_in_list:
            #if((i.shell_money==0) & (i.sd_money==0)):
            #    pass
            #else:
            #    writer.writerow()
            full_name = find_product_full_name(i.ename)
            writer.writerow([i.pname,i.group,i.shop,i.pid,full_name,i.shell_money,i.sd_money,i.wb_money,i.car_money])

if __name__ == "__main__":
    if(kaiguan()):
        print("配置文件正常")
        writer_file()
    else:
        print("无法获取配置文件")
