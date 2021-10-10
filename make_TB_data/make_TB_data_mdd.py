#!/usr/bin/python
#-*- coding : utf-8 -*-

#ps文件需要检测 密码  刚开始的时候需要检测系统是啥

import pandas as pd
import glob,os,openpyxl,re
import urllib.request

man_URL = "d:\\应用\\make_TB_data_mdd\\"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#常用公共方法
def kaiguan():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False

#这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name):
    return glob.glob(r''+man_URL+'file\\*.'+last_name+'')

#判断系统的版本看是linux还是win
#def find_os_version():
#    if(os.name==posix):
#        return "0"
#    else:
#        return "1"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    apk = ["V","v","G","g","_","-","申通","韵达","邮政","顺丰","圆通","'null","极兔","百世","'"]
    try:  
        for a in apk:
            y = y.replace(a,'')
        if(y==""):
            return "备注没名字"
        else:
            return y
    except:
        return "备注没名字"

#获取拼多多文件返回pandas对象
def get_file_pdd():
    name_list = get_file_name_list("xlsx")
    for x in name_list:
        if("已发货查询结果" in x):
            name_list.remove(x)
    shell_data = []
    for x in name_list:
        try:
            shell_data.append(pd.read_excel(x))
        except:
            print("读取pdd销量文件"+x+"出现错误")
    return pd.concat(shell_data)

#获取麦的多文件返回pandas对象
def get_file_mdd():
    name_list1 = get_file_name_list("xlsx") 
    name_list2 = get_file_name_list("xlsx")
    for y in name_list2:
        if("已发货查询结果" not in y):
            name_list1.remove(y)
    shell_data = []
    for x in name_list1:
        try:
            shell_data.append(pd.read_excel(x))
        except:
            print("读取mdd销量文件"+x+"出现错误")
    return pd.concat(shell_data)

#载入人员组简称信息
def get_poople_product_easyname_data():
    pn = pd.read_excel(""+man_URL+"组人简称对应.xlsx")
    zlist = pn["组"].to_list()
    name_list = pn["姓名"].to_list()
    easy_name = pn["简称"].to_list()
    return zlist,name_list,easy_name

def make_data():
    #print(os.name) 这个地方先不要写了注意先要实现功能
    pdd_data = get_file_pdd()
    mdd_data = get_file_mdd()
    #清理重复数据
    mdd_data = mdd_data.drop_duplicates("平台订单号")

    shell_data = pd.merge(pdd_data, mdd_data, how='left', left_on='订单编号', right_on='平台订单号')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #数据处理部分

    #筛选订单状态并且去除已经关闭的订单
    shell_data = shell_data[(shell_data["订单状态_x"]=="卖家已发货，等待买家确认")|(shell_data["订单状态_x"]=="交易成功")|(shell_data["订单状态_x"]=="买家已付款，等待卖家发货")]

    #根据备注生成销售类型·数据
    shell_data['type'] = shell_data.apply(lambda row: return_type(row['订单备注'], row['买家实际支付金额']),axis=1)

    #生成清洗过的备注数据
    shell_data['订单备注2'] = shell_data.订单备注.apply(return_remark)

    #通过外部方法 导入组——姓名——简称数据到内部
    all_list = get_poople_product_easyname_data()
    zlist = all_list[0]
    namelist = all_list[1]
    easy_list = all_list[2]

    def ename_to_name(z):
        for inx , x in enumerate(easy_list):
         if(x in z):
             #print("正确这边是x："+x+"这边是x："+z+"")
             return namelist[inx]
        return "备注没有找到名字"
    def ename_to_group(v):
        for inx , x in enumerate(easy_list):
         if(x in v):
             return zlist[inx]
        return "备注没有找到组"
    shell_data['姓名'] = shell_data.订单备注2.apply(ename_to_name)
    shell_data['组'] = shell_data.订单备注2.apply(ename_to_group)

    #筛选出没有订单的信息
    #shell_data = shell_data.dropna(subset=["操作人"])

    #筛选出真实订单
    #shell_data = shell_data[(shell_data["type"]=="真实")]
   

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #生成数据部分
    #生成店铺统计销量
    shell_data.to_csv(""+man_URL+"all.csv",encoding="utf-8-sig")#生成原始数据方便差错纠错
    
    #生成对应店铺数据
    df1 = shell_data.pivot_table(index=["店铺名称"],values=["买家实际支付金额"],columns= ["type"],aggfunc = 'sum',fill_value=0,margins=1)

    #生成各组数据
    df2 = shell_data.pivot_table(index=["组"],values="买家实际支付金额",aggfunc = 'sum')

    #根据每个人每个店每产品统计销售额
    df3 = shell_data.pivot_table(index=["组","店铺名称","姓名","商品名称"],values = ["买家实际支付金额"],aggfunc = 'sum')

    #外加 ~~~看看能不能统计出销售单品的数量
    with pd.ExcelWriter(r''+man_URL+'result.xlsx') as writer:
        df1.to_excel(writer, sheet_name='每个店铺销售数据',merge_cells=False)
        
        df2.to_excel(writer, sheet_name='每个组销售数据',merge_cells=False)

        df3.to_excel(writer, sheet_name='每人每店每产品销售数据',merge_cells=False)



if __name__ == "__main__":
    if(kaiguan()):
        print("访问正常")
        make_data()
        #read_product_excle()
    else:
        print("无法获取配置文件")