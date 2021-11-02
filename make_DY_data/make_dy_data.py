#!/usr/bin/python
#-*- coding : utf-8 -*-

#计算抖音店铺销量的程序

import pandas as pd
import glob,os,openpyxl,re,platform,datetime
import urllib.request  

man_URL = "d:\\应用\\make_dy_data\\"
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

#将传入的ID前边添加空格
def str_add_space(pID):
    return " "+str(pID)

#这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name):
    return glob.glob(r''+man_URL+'file\\*.'+last_name+'')

def kaiguan():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
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

#判断系统版本然后修改对应的工作路径
def find_version_of_OS():
    sysstr = platform.system()
    global man_URL,shuangxiegang
    if(sysstr =="Windows"):
        get_file_folder()
    elif(sysstr == "Darwin"):
        man_URL = "/Users/tlkzhuo/tlk/git/make_dy_data/"
    else:
        print ("Other System tasks")

#根据系统版本生成相应的路径符号
def return_symbol():
    sysstr = platform.system()
    if(sysstr =="Windows"):
        return "\\"
    elif(sysstr == "Darwin"):
        return "/"
    else:
        return "出错了"
#读取抖音文件并且返回
def  read_shell_file():
    product_file_list =[]
    def get_file_name_list():
        return glob.glob(r''+man_URL+'file'+return_symbol()+'*.csv')
        #print("读取"+str(len(product_file_list))+"个销量数据文件")
 
    #放入list
    for product_file in get_file_name_list():
        try:
            product_file_list.append(pd.read_csv(product_file))
        except:
            print("数据文件"+product_file+"出现错误")
    #返回合并
    shell_data = pd.concat(product_file_list)
    return shell_data[["主订单编号","子订单编号","商品数量","商品ID","商家编码","订单应付金额","订单提交时间","订单完成时间","支付完成时间","订单状态","售后状态","商家备注","旗帜颜色"]]

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

#这是几个拆分套餐名称的对应方法，
def return_combo_name(y):
    try:
        return y.split("+")[0]
    except:
        return y
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

#订单类型判断
def return_type(x,y):
    if(y==1):
        return "活动"
    try:
        if((x.find('V-')!= -1)|(x.find('v-')!= -1)|(x.find('V_')!= -1)|(x.find('v_')!= -1)):
            return "放单"
        elif((x.find('G-')!= -1)|(x.find('g-')!=-1)|(x.find('G_')!= -1)|(x.find('g_')!=-1)):
            return "刷单"
        else:
            return "真实"
    except:
        return "真实"


#读取姓名组ID数据并且返回数据文件
def read_name_data():
    global man_URL,product_ename_and_aname
    xl = pd.read_excel(""+man_URL+"dy产品数据表格.xlsx",None)
    xl_list =[]
    for x in xl.keys():
        xl = pd.read_excel(""+man_URL+"dy产品数据表格.xlsx",x)#读取文件

        if(x.find("组")!= -1):
            #xl['产品ID'] = pd.to_numeric(xl['产品ID'], errors='coerce')#将产品ID转化为数字格式

            #开始清理数据
            xl = xl.loc[:,["店铺","姓名","产品ID"]]#只保留有需要的四列
            xl = xl.dropna(subset=['产品ID']) #删除缺失ID的行
            xl = xl.dropna(axis=0,how='all') #删除为NaN的行

            xl.insert(xl.shape[1], '组', x)#将组名插入到数据里边

            xl_list.append(xl)#将所有的组数据放入list
        #暂时不需要数据类型转换就先注释掉这一块
        elif(x.find("数据")!= -1):
            for row in xl.itertuples():
                pass
                #product_ename_and_aname[getattr(row, '产品简称')] = getattr(row, '产品名称')#载入全称简称转换字典数据
                #如果需要增加转化数据的话可以放在这里
    df = pd.concat(xl_list)
    #清理重复ID部分
    same_id_num = int(df[df.duplicated('产品ID')].count()["产品ID"])#获取重复数量
    if(same_id_num>0):
        print("发现重复记录"+str(same_id_num)+"条")
        print("导出重复记录到默认路径"+day_time("today")+"重复.csv")
        df[df.duplicated('产品ID')].to_csv(""+man_URL+day_time("today")+"重复.csv",index=None)
        return df.drop_duplicates("产品ID")
    else:
        print("没有发现重复的ID")
        return df


def write_data(pd):
    pass

#这块就是处理数据
def make_data():
    shell_data = read_shell_file()#获取销量数据的pd对象
    shell_data['商家编码'] = shell_data['商家编码'].str.strip()
    
    gjpd_ata = add_GJP_file_for_code()#获取管家婆数据的pd对象
    #用销量表链接管家婆数据表格
    shell_data = pd.merge(shell_data, gjpd_ata, how='left', left_on='商家编码', right_on='套餐编码')
    
    #筛选表格订单状态和售后状态
    shell_data = shell_data[(shell_data["订单状态"]=="已完成")|(shell_data["订单状态"]=="已发货")|(shell_data["订单状态"]=="备货中")]
    shell_data = shell_data[(shell_data["售后状态"]=="-")|(shell_data["售后状态"]=="售后关闭")]
    
    #这块需要根据套餐名称拆分多个订单
    #首先标记多个订单的状态~~~这块不写了说不用
    #shell_data['套餐名称type'] = shell_data[(shell_data["套餐名称"].str.contains("+"))]

    #根据套餐名称拆分产品数量单位三个要素需要先筛选加号的信息
    #首先先要过滤加号 然后拆分产品
    shell_data['套餐名_去除合并产品'] = shell_data.套餐名称.apply(return_combo_name)
    shell_data['产品名字'] = shell_data.套餐名_去除合并产品.apply(return_product0)
    shell_data['产品数量'] = shell_data.套餐名_去除合并产品.apply(return_product1)
    #产品数量更换数据类型
    shell_data['产品数量'] =  shell_data['产品数量'].astype("int")
    
    #这块是要判断订单类型
    shell_data['type'] = shell_data.apply(lambda row: return_type(row['商家备注'], row['订单应付金额']),axis=1)

    #获取姓名数据表
    name_data = read_name_data()

    #清理数据商品ID前边的空格
    shell_data['商品ID'] = shell_data['商品ID'].astype(str).str.replace(' ', '')
    #反向清理数据产品ID前边加空格
    #name_data['产品ID_加空格'] = name_data.产品ID.apply(str_add_space)

    #用姓名表格链接 产品表格然后就可以了
    shell_data = pd.merge(shell_data, name_data, how='left', left_on='商品ID', right_on='产品ID')




    #输出全文件，用来检查问题
    shell_data.to_csv(""+man_URL+"all.csv",encoding="utf-8-sig")#生成原始数据方便差错纠错


if __name__ == "__main__":
    if(kaiguan()):
        print("访问正常")
        #开始判断修改操作区路径
        find_version_of_OS()
        print(man_URL)
        make_data()
    else:
        print("无法获取配置文件")