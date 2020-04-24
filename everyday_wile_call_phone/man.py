#-*- coding : utf-8 -*-
#每天筛选整理需要发短信的电话号码并且记录生成当天需要联系的人的电话
import pandas as pd
import numpy as np
import datetime,csv,glob,os


man_url = "d:\\everyday_wile_call_phone\\"

#返回包裹对象
def return_pd_package():
    product_file_list = []
    def get_all_file_list():
        return glob.glob(r''+man_url+'这里放入你下载的文件\\PACKCENTER-EXPORT*.csv')
    for product_file in get_all_file_list():
        product_file_list.append(pd.read_csv(product_file))
    return pd.concat(product_file_list)

#返回订单对象
def return_pd_order():
    product_file_list = []
    def get_all_file_list():
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        return glob.glob(r''+man_url+'这里放入你下载的文件\\*'+now_time+'*.csv')
    for product_file in get_all_file_list():
        product_file_list.append(pd.read_csv(product_file))
    return pd.concat(product_file_list)

# 合并两个对象之后返回差值
def return_today_wile_phone():
    package_pd = return_pd_package()
    package_pd = package_pd[package_pd["包裹状态"]=="已签收"]
    order_pd = return_pd_order()
    order_pd = order_pd[order_pd["订单状态"]=="已发货，待签收"]
    all_pd = pd.merge(package_pd,order_pd,on='订单号')
    all_pd = all_pd[(all_pd["包裹状态"]=="已签收")&(all_pd["订单状态"]=="已发货，待签收")]
    return all_pd


#需要生成的结果文件都需要什么内容   订单号 商品ID 电话  店铺  产品简称
def write_result():
    im_pd = return_today_wile_phone()
    getID_pd = pd.read_excel(""+man_url+"需要打电话产品统计.xlsx")
    oneday_data = pd.merge(im_pd, getID_pd, how='left', left_on='商品id',right_on='产品ID')
    oneday_data = oneday_data[["订单号","商品id","手机","店铺","姓名","产品简称"]]
    oneday_data = oneday_data[oneday_data["姓名"].notnull()]#去除不需要统计的值
    #oneday_data.to_csv(""+man_url+"这里看结果文件\\cha1.csv",sep=',',index=False)

    #获取之前记录的对象的值
    allday_data = pd.read_csv(""+man_url+"all_data.csv")
    oneday_data = oneday_data.append(allday_data)
    oneday_data = oneday_data.append(allday_data)
    oneday_data = oneday_data.drop_duplicates(subset=['订单号'],keep=False)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')

    oneday_data.to_csv(""+man_url+"这里看结果文件\\"+now_time+"需要处理的电话号码.csv",sep=',',index=False)
    #追加差值文件到总数据文件
    allday_data = allday_data.append(oneday_data)
    allday_data.to_csv(""+man_url+"all_data.csv",sep=',',index=False)

    #生成需要发短信的文件
    for row in getID_pd.itertuples():
        pname = getattr(row, '姓名')
        shop = getattr(row, '店铺')
        ename = getattr(row, '产品简称')
        one_product = oneday_data[(oneday_data["姓名"]==pname)&(oneday_data["店铺"]==shop)&(oneday_data["产品简称"]==ename)]
        if(one_product.empty):
            pass
        else:
            with open(""+man_url+"这里看结果文件\\"+now_time+"需要发短信的数据.txt","a+") as f:
                f.write(""+pname+shop+"的"+ename+"\n")
                phone_list = ""
                for row in one_product.itertuples():
                    phone_list = phone_list +","+ str(getattr(row, '手机')).strip()
                f.write(phone_list[1:]+"\n")
                f.close()


    

if __name__ == "__main__":
    write_result()