import pandas as pd
import numpy as np
import time,os,datetime,glob,sys,csv,xlrd
import urllib.request

boy_name = ""
product_list =[]
product_file_list =[]
man_URL = "d:\\应用\\ceshi2\\"
#简称和全称的字典数据
product_ename_and_aname = {}
#直通车数据对象
shell_car_data = ""


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

def read_excle_file():
    mmd_product_file_list =[]
    #获取程序文件夹里边的需要统计的所有文件的数据
    def get_file_name_list():
        return glob.glob(r''+man_URL+'file2\\*.xlsx')
    for mdd_product_file in get_file_name_list():
        try:
            mmd_product_file_list.append(pd.read_excel(mdd_product_file,"已发货查询结果"))
        except:
            print("数据文件"+mdd_product_file+"出现错误")
    #返回合并
    return pd.concat(mmd_product_file_list)

def man():
    shell_pd = get_sell_date_to_pd()
    shell_pd = shell_pd[["订单号","订单状态","商品数量(件)","商品id","商品规格","售后状态","快递单号","快递公司","商家实收金额(元)","商品"]]

    name_pd = read_config_xlsx_new()
    name_pd = name_pd.drop_duplicates("产品ID")
    mmd_pd = read_excle_file()
    mmd_pd = mmd_pd[["店铺","发货类型","平台订单号","商品名称","规格","数量"]]
    mmd_pd = mmd_pd.drop_duplicates("平台订单号")
    shell_pd['订单号'] = shell_pd['订单号'].astype(str)
    shell_pd['商品id'] = shell_pd['商品id'].astype(str).str.extract(r'(\d+)')
    name_pd['产品ID'] = name_pd['产品ID'].astype(str).str.extract(r'(\d+)')
    mmd_pd['平台订单号'] = mmd_pd['平台订单号'].astype(str)


    shell_pd = pd.merge(shell_pd, name_pd, how='left', left_on='商品id', right_on='产品ID',left_index=True)
    shell_pd = shell_pd[(shell_pd["产品简称"]=="HTTGL")|(shell_pd["产品简称"]=="YNBCHYP")]

    mmd_pd = mmd_pd[(mmd_pd["商品名称"]=="HTTGL")|(mmd_pd["商品名称"]=="YNBCHYP")]
    shell_pd = pd.merge(shell_pd, mmd_pd, how='left', left_on='订单号', right_on='平台订单号',left_index=True)
    

    shell_pd.to_csv(""+man_URL+"all.csv",encoding="utf-8-sig")#生成原始数据方便差错纠错
    

if __name__ == "__main__":
    man()
