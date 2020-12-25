#-*- coding : utf-8 -*-
#根据桌面的下载数据统计生成需要的文件发送给会计

import pandas as pd
import time,os,datetime,glob,sys,csv,xlrd
desktop_link = ""
result_file_name = ""
boy_name = ""
product_list =[]
product_file_list =[]

#获取桌面的需要统计的所有文件的数据
def get_file_name_list():
    global product_file_list
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    return glob.glob(r''+desktop_link+'*'+now_time+'*.csv')

#根据所有文件整合数据在一块放入对象
def make_all_file():
    global product_file_list    
    for product_file in get_file_name_list():
        product_file_list.append(pd.read_csv(product_file))
    return pd.concat(product_file_list)

#获取当前文件夹的csv文件找到需要统计的数据
def get_productID_and_productName():
    global product_list
    date = pd.read_csv(""+sys.path[0]+"\\product_name_id.csv")
    for index, row  in date.iterrows():
        print(row[1],index)#这句话不要删除，要不然有黄色的警告真是烦人
        product_list.append({"name":row[0],"id":row[1],"all_shell":0,"rell_shell":0,"make_shell":0,"money_car":0})
    return product_list

#获取当前文件夹的csv文件找到需要统计的数据
def get_link_and_filename():
    global product_list,desktop_link,result_file_name,boy_name
    date = pd.read_csv(""+sys.path[0]+"\\content.csv")
    for index, row  in date.iterrows():
        print(row[0],index)#这句话不要删除，要不然有黄色的警告真是烦人
        if(row[0]=="desktop_link"):
            desktop_link = row[1]
        if(row[0]=="file_name"):
            result_file_name = row[1]
        if(row[0]=="boy_name"):
            boy_name = row[1]
    return product_list

#直通车花费统计直接通过ID找到花费金额
def get_money_car(productID):
    car_money_file_list=[]
    car_money_pd =[]
    yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    yes_time = yes_time.strftime('%Y%m%d')
    try:
        car_money_file_list = glob.glob(r''+desktop_link+'*_账户_分级详情_计划_'+yes_time+'*.xls')
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

def writer_file():
    global result_file_name,boy_name
    get_link_and_filename()#获取配置文件信息并且载入
    result_file = make_all_file()
    all_date = result_file[(result_file["售后状态"]=="无售后或售后取消")|(result_file["售后状态"]=="售后处理中")]
    all_date = all_date[(all_date["订单状态"]=="待发货")|(all_date["订单状态"]=="已发货，待签收")|(all_date["订单状态"]=="已签收")]
    #all_date["商家备注"] = all_date["商家备注"].str.split(";").str[-1]
    for one_date in get_productID_and_productName():
        all_shell = all_date[(all_date["商品id"]==one_date['id'])]["商家实收金额(元)"].sum()
        make_shell = all_date[(all_date["商品id"]==one_date['id'])&(all_date["商家备注"].str.contains("G-"))]["商家实收金额(元)"].sum()
        wb_make_shell = all_date[(all_date["商品id"]==one_date['id'])&(all_date["商家备注"].str.contains("V-"))]["商家实收金额(元)"].sum()
        one_date["all_shell"] = round(all_shell,2)
        one_date["make_shell"] = round(make_shell+wb_make_shell,2)
        one_date["rell_shell"] = round(all_shell-(make_shell+wb_make_shell),2)
        one_date["money_car"] = get_money_car(str(one_date['id']))
        print(one_date)

    yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    #yes_time_nyr = yes_time.strftime('%Y_%m_%d')
    yes_time = yes_time.strftime('%Y-%m-%d')

    with open(""+desktop_link+result_file_name,"a+",newline = '') as csvfile: 
        writer = csv.writer(csvfile)
        for i in product_list:
            if(i["all_shell"]==0):
                pass
            else:
                writer.writerow([yes_time,boy_name,i["name"].split("店")[0],i["name"].split("店")[1],i["all_shell"],i["make_shell"],i["money_car"],i["rell_shell"],round(i["rell_shell"]-(i["money_car"]),2)])
            
if __name__ == "__main__":
    writer_file()
