#-*- coding : utf-8 -*-
#之前的太乱了往后整合到一块去
#重复筛选提醒

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
#简称和全称的字典数据
product_ename_and_aname = {}
#直通车数据对象
shell_car_data = ""




#根据所有文件整合数据在一块放入对象
def make_all_file():
    #获取程序文件夹里边的需要统计的所有文件的数据
    def get_file_name_list():
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
    all_date = all_date[(all_date["订单状态"]=="待发货")|(all_date["订单状态"]=="已发货，待签收")|(all_date["订单状态"]=="已签收")]
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

#======================华丽的分割线======================

#获取时间比较多就放在一块了
def day_time(day):
    today_time = datetime.datetime.now()
    today_time = today_time.strftime('%Y%m%d')
    yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    yes_time = yes_time.strftime('%Y%m%d')
    if(day=="today"):
        return today_time 
    elif(day=="yestday"):
        return yes_time
    else:
        return False
    
#这个方法是检测相同的ID的方法
def find_same_ID(df):
    same_id_num = int(df[df.duplicated('产品ID')].count()["产品ID"])#获取重复数量
    if(same_id_num>0):
        print("发现重复记录"+str(same_id_num)+"条")
        print("导出重复记录到默认路径"+day_time("today")+"重复.csv")
        df[df.duplicated('产品ID')].to_csv(""+man_URL+day_time("today")+"重复.csv")
        return df.drop_duplicates("产品ID")
    else:
        print("没有发现重复的ID")
        return df

#读取配置文件分成两部分第一部分吧组数据放在一个对象了里，第二部分把所有的其他的
def read_config_xlsx_new():
    global man_URL,product_ename_and_aname
    xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",None)
    xl_list =[]
    for x in xl.keys():
        xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",x)#读取文件

        if(x.find("组")!= -1):
            xl['产品ID'] = pd.to_numeric(xl['产品ID'], errors='coerce')#将产品ID转化为数字格式

            #开始清理数据
            xl = xl.loc[:,["店铺","产品简称","姓名","产品ID"]]#只保留有需要的四列
            xl = xl.dropna(subset=['产品ID']) #删除确实ID的行
            xl = xl.dropna(axis=0,how='all') #删除为NaN的行

            xl.insert(xl.shape[1], '组', x)#将组名插入到数据里边

            xl_list.append(xl)#将所有的组数据放入list
        elif(x.find("数据")!= -1):
            for row in xl.itertuples():
                product_ename_and_aname[getattr(row, '产品简称')] = getattr(row, '产品名称')#载入全称简称转换字典数据
                #如果需要增加转化数据的话可以放在这里
    df = pd.concat(xl_list)
    #清理重复ID部分
    same_id_num = int(df[df.duplicated('产品ID')].count()["产品ID"])#获取重复数量
    if(same_id_num>0):
        print("发现重复记录"+str(same_id_num)+"条")
        print("导出重复记录到默认路径"+day_time("today")+"重复.csv")
        df[df.duplicated('产品ID')].to_csv(""+man_URL+day_time("today")+"重复.csv")
        return df.drop_duplicates("产品ID")
    else:
        print("没有发现重复的ID")
        return df

#读取所有的销量文件放在一块不需要筛选时间
def get_sell_date_to_pd():
    #获取程序文件夹里边的需要统计的所有文件的数据
    def get_file_name_list():
        return glob.glob(r''+man_URL+'file\\*.csv')
    global product_file_list
    print("读取"+str(len(product_file_list))+"个销量数据文件")
    #放入list
    for product_file in get_file_name_list():
        try:
            product_file_list.append(pd.read_csv(product_file))
        except:
            print("数据文件"+product_file+"出现错误")
    #返回合并
    return pd.concat(product_file_list)

#建立直通车的pandas对象
def get_car_data_to_pd():
    global shell_car_data
    car_money_file_list=[]#初始化文件路径list
    car_money_pd =[]#初始化直通车数据对象list
    car_money_file_list = glob.glob(r''+man_URL+'file\\*.xls')#获取所有的直通车文件list
    print("总共需要处理"+len(car_money_file_list)+"个直通车文件")
    for x in car_money_file_list:
        try:
            car_money_pd.append(pd.read_excel(x))
        except:
            print("直通车文件"+x+"出现错误")
    shell_car_data = pd.concat(car_money_pd)

#通过这个方法可以查询直通车的数据
def find_carmoney_data(productID):
    global shell_car_data
    one_resultpd = shell_car_data[(shell_car_data['推广计划'].str.find(productID, start=0, end=None)>=0)]
    if(len(one_resultpd)):
        return one_resultpd["花费(元)"].sum()
    else:
        return 0

#这块是通过各类数据开始计算结果
def compute_result(df,shell_date):
    #筛选需要统计的销量信息
    shell_date = shell_date[(shell_date["售后状态"]=="无售后或售后取消")|(shell_date["售后状态"]=="售后处理中")]
    shell_date = shell_date[(shell_date["订单状态"]=="待发货")|(shell_date["订单状态"]=="已发货，待签收")|(shell_date["订单状态"]=="已签收")]

    shell_date["商品id"].astype("str")
    #遍历掉df 然后插入当前ID的销售额放单刷单直通车和生成扣直通车和刷单放单之后的销售额
    for df, row in df.iterrows:
        pass


    
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



#检测执行步骤到哪一步卡死了
def content():
    print("载入配置文件")
    df = read_config_xlsx_new()
    print("开始载入销量数据")
    shell_date = get_sell_date_to_pd()
    print("载入直通车数据")
    get_car_data_to_pd()
    print("开始计算")
    compute_result(df,shell_date)
    print("需要说明计算方法")

    print("开始生成结果")

#主函数
if __name__ == "__main__":
    content()
