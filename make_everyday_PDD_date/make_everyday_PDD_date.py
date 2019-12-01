#-*- coding : utf-8 -*-
#根据桌面的下载数据统计生成需要的文件发送给会计

import pandas as pd
import time,os,datetime,glob,sys,csv
desktop_link = "C:\\Users\\Administrator\\Desktop\\"
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



if __name__ == "__main__":
    result_file = make_all_file()
    all_date = result_file[result_file["售后状态"]=="无售后或售后取消"]
    all_date["商家备注"] = all_date["商家备注"].str.split(";").str[-1]
    for one_date in get_productID_and_productName():
        all_shell = all_date[(all_date["商品id"]==one_date['id'])]["商家实收金额(元)"].sum()
        make_shell = all_date[(all_date["商品id"]==one_date['id'])&(all_date["商家备注"].str.contains("G-"))]["商家实收金额(元)"].sum()
        one_date["all_shell"] = round(all_shell,2)
        one_date["make_shell"] = round(make_shell,2)
        one_date["rell_shell"] = round(all_shell-make_shell,2)
        print(one_date)

    yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    yes_time_nyr = yes_time.strftime('%Y_%m_%d')

    with open(""+desktop_link+"郭文卓每日数据.csv","a+",newline = '') as csvfile: 
        writer = csv.writer(csvfile)
        #写入标题
        writer.writerow([""+yes_time.strftime('%Y-%m-%d')+"日销售数据如下"])
        #先写入columns_name
        writer.writerow(["产品名字","总销售额","真实销售额","干预销售额","直通车消耗"])
        #写入多行用writerows
        for i in product_list:
            writer.writerow([i["name"],i["all_shell"],i["rell_shell"],i["make_shell"],0])

