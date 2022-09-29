#!/usr/bin/python
#-*- coding : utf-8 -*-

#ps到时候需要检测文件的密码

import pandas as pd
import glob,os,openpyxl,re
import urllib.request   

man_URL = "d:\\应用\\ceshi12\\"
shell_car_data = ""


#这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name):
    return glob.glob(r''+man_URL+'file\\*.'+last_name+'')

#判断这个对象是刷单还是正常销售
def return_type(x,yz):
    if(yz==1):
        return "一元"
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
    apk = ["V","v","G","g","_","-","申通","韵达","邮政","顺丰","圆通","'null","极兔"]
    try:  
        for a in apk:
            y = y.replace(a,'')
        if(y==""):
            return "备注没名字"
        else:
            return y
    except:
        return "备注没名字"
def return_product0(z):
    try:
        z = re.split(r'(\d+)',z)[0]
        return z
    except:
        return "后台没写套餐编码"
def return_product1(z):
    try:
        z = re.split(r'(\d+)',z)[1]
        return z
    except:
        return 1
def return_product2(z):
    try:
        z = re.split(r'(\d+)',z)[2]
        return z
    except:
        return z

#吧是商品编码的变成套餐编码
def return_code(w):
    if(str(w).count("-")==1):
        w = w + "-1"
    elif(str(w).count("-")==0):
        w = "no"
    return w    

def kaiguan():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#读取产品数据表格做三个映射
def read_product_excle():
    xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",sheet_name="数据")
    x_Pname = xl[["姓名","姓名代码"]].dropna(axis=0,how='all')
    x_product_name = xl[["产品名称","产品简称"]].dropna(axis=0,how='all')
    x_shop_name = xl[["淘宝特价版店铺","特价版对应小组"]].dropna(axis=0,how='all')
    return [x_Pname,x_product_name,x_shop_name]
 
#读取读取并且合并多个管家婆下载的文件
def add_GJP_file_for_code():
    global shell_car_data
    print("开始读取管家婆数据")
    xl_list = get_file_name_list("xls")
    gjp_list = []
    for x in xl_list:
        try:
            gjp_list.append(pd.read_excel(x,skiprows=10))
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
    shell_data2["主订单编号"] = shell_data2["主订单编号"].map(lambda x: str(x).lstrip('=').rstrip('=')).astype(str)
    shell_data2["主订单编号"] = shell_data2["主订单编号"].map(lambda x: str(x).lstrip('"').rstrip('"')).astype(str)
    #清楚宝贝表的重复数据
    shell_data2 = shell_data2.drop_duplicates("主订单编号")
    #合并数据表和宝贝表
    shell_data = pd.merge(shell_data, shell_data2, how='left', left_on='订单编号',right_on='主订单编号')
    #print(shell_data[shell_data["买家会员名"]=="走俏宝贝"])
    #返回数据
    return shell_data

#生成数据
def make_data():
    #载入数据
    shell_data = get_shell_data()
    gjp_data = add_GJP_file_for_code()

    #筛选订单
    #筛选订单状态并且去除已经关闭的订单
    shell_data = shell_data[(shell_data["订单状态_x"]=="卖家已发货，等待买家确认")|(shell_data["订单状态_x"]=="交易成功")|(shell_data["订单状态_x"]=="买家已付款，等待卖家发货")]
    #去除销量是1的订单    
    #shell_data = shell_data[(shell_data["买家实际支付金额"]!=1)]

    #有些写的是商品编码 不是套餐编码那么就转换成套餐编码
    shell_data['商家编码2'] = shell_data.商家编码.apply(return_code)
    #链接管家婆表格
    shell_data = pd.merge(shell_data, gjp_data, how='left', left_on='商家编码2', right_on='套餐编码')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #数据处理部分
    #根据备注生成销售类型·数据
    shell_data['type'] = shell_data.apply(lambda row: return_type(row['商家备忘'], row['买家实际支付金额_x']),axis=1)
    #根据销售金额判断是不是1元够
    #shell_data['type2'] = shell_data.买家实际支付金额.apply(return_type2)



    #生成清洗过的备注数据
    shell_data['商家备忘2'] = shell_data.商家备忘.apply(return_remark)
    
    #拆分套餐信息
    #shell_data['套餐名'] = shell_data["套餐名称"].map(lambda x : (re.split(r'(\d+)',x)[0]))#这是另外一个方法不要写没办法写try except 先放弃
    shell_data['套餐名'] = shell_data.套餐名称.apply(return_product0)
    shell_data['套餐数量'] = shell_data.套餐名称.apply(return_product1)
    shell_data['套餐单位'] = shell_data.套餐名称.apply(return_product2)
    shell_data['套餐数量'] =  shell_data['套餐数量'].astype("int")

    #映射几个数据

    xpd = read_product_excle()
    x_Pname = xpd[0]
    x_product_name = xpd[1]
    x_shop_name = xpd[2]

    #翻译姓名代码如果没有找到就返回原来的值
    def easy_name_to_name(name1,name2):
        #print("name1:"+str(name1)+"name2:"+str(name2)+"")
        if(pd.isnull(name2)):#判断姓名里边是否有数据
            return name1
        else:
            return name2

    shell_data = pd.merge(shell_data, x_Pname, how='left', left_on='商家备忘2', right_on='姓名代码')
    shell_data['商家备忘3'] = shell_data.apply(lambda row: easy_name_to_name(row['商家备忘2'], row['姓名']),axis=1)
    shell_data = pd.merge(shell_data, x_product_name, how='left', left_on='套餐名', right_on='产品简称')
    shell_data = pd.merge(shell_data, x_shop_name, how='left', left_on='店铺名称', right_on='淘宝特价版店铺')



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #生成数据部分
    #生成店铺统计销量
    shell_data.to_csv(""+man_URL+"all.csv",encoding="utf-8-sig")#生成原始数据方便差错纠错

    df1 = shell_data.pivot_table(index=["特价版对应小组","店铺名称","type"],values="买家实际支付金额_x",aggfunc = 'sum')
    
    #生成没有备注的店铺和订单
    df2 = shell_data[(shell_data["商家备忘"].isnull())|(shell_data["商家备忘"]=="null")]

    #df2 = shell_data[(shell_data["商家备忘"]=="")]
    df2 = df2[["店铺名称","订单编号","商家备忘"]]

    #根据每个人每个店每产品统计销售额
    df3 = shell_data.pivot_table(index=["特价版对应小组","店铺名称","商家备忘3","产品名称","type"],values = ["买家实际支付金额_x","套餐数量"],aggfunc = 'sum')

    #外加 ~~~看看能不能统计出销售单品的数量
    with pd.ExcelWriter(r''+man_URL+'result.xlsx') as writer:
        df1.to_excel(writer, sheet_name='每个店铺销售数据',merge_cells=False)
        if(len(df2)):
            df2.to_excel(writer, sheet_name='没有备注的订单')
        else:
            print("kong")
        df3.to_excel(writer, sheet_name='每人每店每产品销售数据',merge_cells=False)
        

if __name__ == "__main__":
    if(kaiguan()):
        print("访问正常")
        make_data()
        #read_product_excle()
    else:
        print("无法获取配置文件")
