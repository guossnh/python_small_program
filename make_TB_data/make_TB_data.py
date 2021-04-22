#!/usr/bin/python
#-*- coding : utf-8 -*-
#主要是拼合文件csvt特殊表头的文件

#到时候需要检测文件的密码

import pandas as pd
import glob,os,openpyxl
import urllib.request   

man_URL = "d:\\应用\\make_TB_data\\"
shell_car_data = ""

 
#这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name):
    return glob.glob(r''+man_URL+'file\\*.'+last_name+'')

#判断这个对象是刷单还是正常销售
def return_type(x):
    try:
        if((x.find('V-')!= -1)|(x.find('v-')!= -1)|(x.find('V_')!= -1)|(x.find('v_')!= -1)):
            return "放单"
        elif((x.find('G-')!= -1)|(x.find('g-')!=-1)|(x.find('G_')!= -1)|(x.find('g_')!=-1)):
            return "刷单"
        else:
            return "真实"
    except:
        return "真实"

#清洗商家备注
def return_remark(y):
    #抹去的字符串 
    apk = ["V","v","G","g","_","-","申通","韵达","邮政","顺丰","圆通"]
    try:
        for a in apk:
            y = y.replace(a,'')
        return y
    except:
        return ""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#读取读取并且合并多个管家婆下载的文件
def add_GJP_file_for_code():
    global shell_car_data
    print("开始读取管家婆数据")
    xl_list = get_file_name_list("xls")
    gjp_list = []
    for x in xl_list:
        try:
            gjp_list.append(pd.read_excel(x,skiprows=11))
        except:
            print("读取管家婆文件"+x+"出现错误")
    shell_car_data = pd.concat(gjp_list)
    shell_car_data = shell_car_data[["套餐名称","套餐编码"]]
    return shell_car_data


#这个 方法主要就是并且把产品编码和sku名称拿出来予以对应返
def get_sku_name_from_code(code):
    #https://blog.csdn.net/w55100/article/details/90145191
    #可以上边的页面 先测试再查找坐标
    global shell_car_data
    shell_car_data[shell_car_data["套餐编码"]==code].index.tolist()

    
    #判断数组是不是为空如

#获取销量数据
def get_shell_data():
    shell_data_list = get_file_name_list("xlsx")
    shell_data_list2 = get_file_name_list("csv")
    shell_data = []
    shell_data2 = []
    for x in shell_data_list:
        try:
            shell_data.append(pd.read_excel(x))
        except:
            print("读取销量文件"+x+"出现错误")
    for a in shell_data_list2:
        try:
            shell_data2.append(pd.read_csv(a,encoding="gbk"))
        except:
            print("读取宝贝文件"+a+"出现错误")
    shell_data = pd.concat(shell_data)
    shell_data2 = pd.concat(shell_data2)
    #转换需要的数据格式并且去除特殊字符
    shell_data["订单编号"] = shell_data["订单编号"].astype(str)
    shell_data2["订单编号"] = shell_data2["订单编号"].map(lambda x: str(x).lstrip('=').rstrip('=')).astype(str)
    shell_data2["订单编号"] = shell_data2["订单编号"].map(lambda x: str(x).lstrip('"').rstrip('"')).astype(str)
    #合并数据表和宝贝表
    shell_data = pd.merge(shell_data, shell_data2, how='left', on='订单编号')
    #返回数据
    return shell_data

def make_data():
    shell_data = get_shell_data()
    gjp_data = add_GJP_file_for_code()
    #筛选订单状态并且去除已经关闭的订单
    shell_data = shell_data[(shell_data["订单状态_x"]=="卖家已发货，等待买家确认")|(shell_data["订单状态_x"]=="交易成功")]
    
    shell_data = shell_data[(shell_data["买家实际支付金额"]!=1)]
    #链接管家婆表格
    shell_data = pd.merge(shell_data, gjp_data, how='left', left_on='商家编码', right_on='套餐编码')

    #更具备注生成销售类型·数据
    shell_data['type'] = shell_data.商家备忘.apply(return_type)
    #清洗备注数据 
    shell_data['商家备忘2'] = shell_data.商家备忘.apply(return_remark)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #生成店铺统计销量
    df1 = shell_data.pivot_table(index="店铺名称",values="买家实际支付金额",aggfunc = 'sum')
    
    #生成没有备注的店铺和订单
    df2 = shell_data[(shell_data["商家备忘"].isnull())|(shell_data["商家备忘"]=="null")]
    #df2 = shell_data[(shell_data["商家备忘"]=="")]
    df2 = df2[["店铺名称","订单编号","商家备忘"]]

    #根据每个人每个店每产品统计销售额
    df3 = shell_data.pivot_table(index=["店铺名称","商家备忘2","套餐名称","type"],values="买家实际支付金额",aggfunc = 'sum')

    shell_data.to_csv(""+man_URL+"wocao.csv")
    #外加 ~~~看看能不能统计出销售单品的数量
    with pd.ExcelWriter(r''+man_URL+'result.xlsx') as writer:
        df1.to_excel(writer, sheet_name='每个店铺销售数据')
        if(len(df2)):
            df2.to_excel(writer, sheet_name='没有备注的订单')
        else:
            print("kong")
        df3.to_excel(writer, sheet_name='每人每店每产品销售数据')
        

if __name__ == "__main__":
    make_data()#调用主要方法
