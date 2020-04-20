#-*- coding : utf-8 -*-
#根据固定文件夹下边整理的全公司的销售数据和直通车数据共同计算出最终结果。

import pandas as pd
import time,os,datetime,glob,sys,csv,xlrd
boy_name = ""
product_list =[]
product_file_list =[]
man_URL = "d:\\make_everyday_PDD_date_for_XYL\\"
product_link_in_list = []#这个是所有产品信息对象的存储


#根据所有文件整合数据在一块放入对象
def make_all_file():
    #获取桌面的需要统计的所有文件的数据
    def get_file_name_list():
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        return glob.glob(r''+man_URL+'file\\*'+now_time+'*.csv')
    global product_file_list
    for product_file in get_file_name_list():
        product_file_list.append(pd.read_csv(product_file))
    return pd.concat(product_file_list)

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
            return one_resultpd["花费(元)"].values[0]
        else:
            return 0
    except:
        return 0

#读取配置放产品对象进入对象的数组
def read_config_xlsx():
    global man_URL,product_link_in_list
    #读取文件并且获取组列表
    xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",None)
    #去掉数据表格其他的表格名字加入Class_leader
    for x in xl.keys():
        if(x.find("组")!= -1):
            xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",x)
            for row in xl.itertuples():
                #print(getattr(row, '店铺'), getattr(row, '产品简称'))
                product_link_in_list.append(product_link_in(getattr(row, '产品ID'),getattr(row, '店铺'),getattr(row, '产品简称'),getattr(row, '姓名'),0,0,0,x))
    return product_link_in_list


#这个是对应每一个产品链接的对象，包括直通车数据，销售额，刷单
class product_link_in:
    def __init__(self,pid,shop,ename,pname,car_money,shell_money,sd_money,group):
        self.pid = pid
        self.shop = shop
        self.ename = ename
        self.pname = pname
        self.car_money = car_money
        self.shell_money = shell_money
        self.sd_money = sd_money
        self.group = group

def writer_file():
    global boy_name
    result_file = make_all_file()
    all_date = result_file[(result_file["售后状态"]=="无售后或售后取消")|(result_file["售后状态"]=="售后处理中")]
    all_date["商家备注"] = all_date["商家备注"].str.split(";").str[-1]
    for one_date in read_config_xlsx():
        all_shell = all_date[(all_date["商品id"]==one_date.pid)]["商家实收金额(元)"].sum()
        wb_make_shell = all_date[(all_date["商品id"]==one_date.pid)&(all_date["商家备注"].str.contains("V-"))]["商家实收金额(元)"].sum()
        one_date.sd_money = round(wb_make_shell,2)
        one_date.shell_money = round(all_shell-wb_make_shell,2)
        one_date.car_money = get_money_car(str(one_date.pid))
        #print(one_date.pid,one_date.car_money,one_date.shell_money,one_date.sd_money,one_date.group)

    with open(""+man_URL+"result.csv","w",newline = '') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["姓名","组","店","产品ID","产品简称","销量","刷单","直通车"])
        for i in product_link_in_list:
            #if((i.shell_money==0) & (i.sd_money==0)):
            #    pass
            #else:
            #    writer.writerow()
            writer.writerow([i.pname,i.group,i.shop,i.pid,i.pname,i.shell_money,i.sd_money,i.car_money])



if __name__ == "__main__":
    writer_file()