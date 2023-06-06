#-*- coding : utf-8 -*-
#京东的计算程序

import pandas as pd
import numpy as np
import time,os,datetime,glob,sys,csv,xlrd,re
import urllib.request

man_URL = "e:\\应用\\ceshi18\\"
product_ename_and_aname = {}


#======================通用方法======================
#获取时间比较多就放在一块了
def day_time(day):
    today_time = datetime.datetime.now()
    today_time = today_time.strftime('%Y%m%d')
    yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    yes_time = yes_time.strftime('%Y%m%d' )
    if(day=="today"):
        return today_time 
    elif(day=="yestday"):
        return yes_time
    else:
        return False

#获取执行程序的文件夹的路径
def get_file_folder():
    #fielpath = os.getcwd()
    global man_URL
    folder_list = os.listdir(os.path.dirname(__file__))
    if("file" in folder_list):
        print("修改工作路径")
        man_URL = os.path.dirname(__file__).replace("\\","\\\\")+"\\\\"
    else:
        print("调试路径")

#这个是判断网络链接的方法 
def kaiguan2():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False

#读取配置文件分成两部分第一部分吧组数据放在一个对象了里，第二部分把所有的其他的
def read_config_xlsx_new():
    global man_URL,product_ename_and_aname
    xl = pd.read_excel(""+man_URL+"京东产品数据表格.xlsx",None)
    xl_list =[]
    for x in xl.keys():
        xl = pd.read_excel(""+man_URL+"京东产品数据表格.xlsx",x)#读取文件

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
        return glob.glob(r''+man_URL+'file\\*.xlsx')
    product_file_list = []
    print("读取"+str(len(get_file_name_list()))+"个销量数据文件")
    #放入list
    for product_file in get_file_name_list():
        try:
            product_file_list.append(pd.read_excel(product_file))
        except:
            print("数据文件"+product_file+"出现错误")
    #返回合并
    shell_data = pd.concat(product_file_list)
    shell_data = shell_data[["订单号","商品ID","订购数量","下单时间","结算金额","订单状态","商家备注","付款确认时间"]]
    return shell_data

#创建一个方法用来区分单条数据是干预，真实，网站放单
def return_type(x):
    try:
        if((x.find('V-')!= -1)|(x.find('v-')!= -1)):
            return 1
        elif((x.find('G-')!= -1)|(x.find('g-')!=-1)):
            return 2
        else:
            return 0
    except:
        return 0

#这块是把产品明细读取一下加入数据表
def get_product_price_file():
    global man_URL
    x2 = pd.read_excel(""+man_URL+"产品明细.xlsx")
    x2 = x2[["产品简称","成本价格"]]#只保留有需要的两列
    x2 = x2.rename(columns={'产品简称':'产品简称2'})
    #清理重复数据
    x2 = x2.drop_duplicates("产品简称2")
    return x2
#======================计算方法======================
def compute_result(shell_data,P_data):
    #筛选需要统计的销量信息
    shell_data = shell_data[(shell_data["订单状态"]=="等待确认收货")|(shell_data["订单状态"]=="完成")]
    #清理ID数据
    shell_data['商品ID'] = shell_data['商品ID'].astype(str).str.extract(r'(\d+)')

    #清理ID数据
    P_data['产品ID'] = P_data['产品ID'].astype(str).str.extract(r'(\d+)')

    #添加商品有效销量计数，
    shell_data["计数"] = 1

    #总共销量表格加入type区分干预，真实，网站放单
    shell_data['type'] = shell_data.商家备注.apply(return_type)

    #在df表里边加入各种销量数据
    v_shell_data = shell_data[shell_data['type']==1]
    g_shell_data = shell_data[shell_data['type']==2]
    t_shell_data = shell_data[shell_data['type']==0]
    P_data['销量'] = P_data.产品ID.apply(lambda x : t_shell_data.结算金额.loc[t_shell_data.商品ID == x].sum())
    P_data['干预'] = P_data.产品ID.apply(lambda x : g_shell_data.结算金额.loc[g_shell_data.商品ID == x].sum())
    P_data['放单'] = P_data.产品ID.apply(lambda x : v_shell_data.结算金额.loc[v_shell_data.商品ID == x].sum())
    P_data['订单发货数量'] = P_data.产品ID.apply(lambda x : shell_data.计数.loc[shell_data.商品ID == x].sum())
    #先要筛选出真实的和放单的shell_data对象
    shell_data_v_t = shell_data[(shell_data['type']==1)|(shell_data['type']==0)]
    P_data['订单发货数量（放+真）'] = P_data.产品ID.apply(lambda x : shell_data_v_t.计数.loc[shell_data_v_t.商品ID == x].sum())

    return P_data

#写出文件
def write_file(df):
    global man_URL
    #调整列位置开始输出
    df = df[["店铺","产品简称","姓名","产品ID","组","销量","干预","放单","订单发货数量","订单发货数量（放+真）"]]
    #df.to_csv(""+man_URL+day_time('today')+"result.csv",index=False,encoding="utf-8-sig",columns=['店铺','产品简称','商品全称','姓名','产品ID','组','销量','干预','放单','直通车'])
    df.to_csv(""+man_URL+day_time('today')+"result.csv",index=False,encoding="utf-8-sig")

#======================华丽的分割线======================


if __name__ == "__main__":
    if(kaiguan2()):
        
        print("访问正常")
        #开始判断修改操作区路径
        get_file_folder()
        #读取订单数据文件
        shell_data = get_sell_date_to_pd()
        #读取ID商品对应文件
        P_data = read_config_xlsx_new()
        #开始把数据合在一块开始计算
        df = compute_result(shell_data,P_data)
        print("开始生成结果")
        write_file(df)
        print("结束了")
        os.system('pause')
        os.system("explorer.exe %s" % ""+man_URL+"")



    else:
        print("无法获取配置文件")
