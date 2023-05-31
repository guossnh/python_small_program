#-*- coding : utf-8 -*-
#新版的淘宝这边的程序计算。
#拼多多有的功能大约都要添加一下  合拍单子的情况需要根据比例计算清楚


import pandas as pd
import numpy as np
import time,os,datetime,glob,sys,csv,xlrd,re
import urllib.request


boy_name = ""
product_list =[]
product_file_list =[]
man_URL = "E:\\应用\\ceshi16\\"
#简称和全称的字典数据
product_ename_and_aname = {}

#==========================================基础部分==========================================
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

#这个方法是检测相同的ID的方法
def find_same_ID(df):
    same_id_num = int(df[df.duplicated('产品ID')].count()["产品ID"])#获取重复数量
    if(same_id_num>0):
        print("发现重复记录"+str(same_id_num)+"条")
        print("导出重复记录到默认路径"+day_time("today")+"重复的ID.csv")
        df[df.duplicated('产品ID')].to_csv(""+man_URL+day_time("today")+"重复.csv")
        return df.drop_duplicates("产品ID")
    else:
        print("没有发现重复的ID")
        return df

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

#这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name,folder='file'):
    return glob.glob(r''+man_URL+''+folder+'\\*.'+last_name+'')

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

#清洗ID数据
def return_clear_id(z):
    try:
        #z = re.split(r'(\d+)',z)[1]
        z = re.findall(r'(\d+)',str(z))
        return z[0]
    except:
        return "商品ID出错"

def return_clear_id2(z):
    try:
        z = str(z)
        z = z.split(".")[0]
        return z
    except:
        return "产品ID错误"

#==========================================逻辑部分==========================================
#根据简称检索全称并且返回
def find_product_full_name2(easyname):
    global product_ename_and_aname
    try:
        return product_ename_and_aname[easyname]
    except:
        return easyname

#这个是判断网络链接的方法 
def kaiguan2():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False

#这块是把产品明细读取一下加入数据表
def get_product_price_file():
    global man_URL
    x2 = pd.read_excel(""+man_URL+"产品明细.xlsx")
    x2 = x2[["产品简称","成本价格"]]#只保留有需要的两列
    x2 = x2.rename(columns={'产品简称':'产品简称2'})
    #清理重复数据
    x2 = x2.drop_duplicates("产品简称2")
    return x2

#读取读取并且合并多个管家婆下载的文件
def add_GJP_file_for_code():
    global shell_car_data

    #读取相应文件夹下边的所有xls格式文件
    def get_file_name_list(last_name):
        return glob.glob(r''+man_URL+'gjp\\*.'+last_name+'')

    print("开始读取管家婆数据")
    xl_list = get_file_name_list("xls")
    gjp_list = []
    for x in xl_list:
        try:
            gjp_list.append(pd.read_excel(x,skiprows=10))
        except:
            print("读取管家婆文件"+x+"出现错误")
    shell_gjp_data = pd.concat(gjp_list)
    shell_gjp_data = shell_gjp_data[["套餐名称","套餐编码"]]
    return shell_gjp_data

#读取配置文件分成两部分第一部分吧组数据放在一个对象了里，第二部分把所有的其他的
def read_config_xlsx_new():
    global man_URL,product_ename_and_aname
    xl = pd.read_excel(""+man_URL+"产品数据表格淘宝.xlsx",None)
    xl_list =[]
    for x in xl.keys():
        xl = pd.read_excel(""+man_URL+"产品数据表格淘宝.xlsx",x)#读取文件

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
        return glob.glob(r''+man_URL+'file\\*.csv')
    global product_file_list
    print("读取"+str(len(get_file_name_list()))+"个销量数据文件")
    #放入list
    for product_file in get_file_name_list():
        try:
            product_file_list.append(pd.read_csv(product_file,encoding='GB18030'))
        except:
            print("数据文件"+product_file+"出现错误")
    #返回合并
    return pd.concat(product_file_list)

#这块是通过各类数据开始计算结果
def compute_result(df,shell_data):
    global shell_car_data
    #筛选需要统计的销量信息
    shell_data = shell_data[(shell_data["订单状态"]=="交易成功")|(shell_data["订单状态"]=="买家已付款，等待卖家发货")|(shell_data["订单状态"]=="卖家已发货，等待买家确认")]

    #修改数据类型方便判断
    shell_data["子订单编号"].astype("str")

    #添加商品有效销量计数，
    shell_data["计数"] = 1
    #添加统计有效快递的列
    shell_data["有效快递"] = 1


    #获取管家婆数据
    gjp_data = add_GJP_file_for_code()
    #首先清理管家婆数据再合并表格
    gjp_data = gjp_data.drop_duplicates("套餐编码")
    #用销量表链接管家婆数据表格
    shell_data = pd.merge(shell_data, gjp_data, how='left', left_on='商家编码', right_on='套餐编码')

    #因为商品ID格式问题 首先清理商品IDreturn_clear_id
    shell_data['商品id'] = shell_data.商品id.apply(return_clear_id)
    df['产品ID'] = df.产品ID.apply(return_clear_id2)


    #根据套餐名称拆分产品数量单位三个要素需要先筛选加号的信息
    #首先先要过滤加号 然后拆分产品
 
    shell_data['套餐名_去除合并产品'] = shell_data.套餐名称.apply(return_combo_name)
    shell_data['产品名字'] = shell_data.套餐名_去除合并产品.apply(return_product0)
    shell_data['产品数量'] = shell_data.套餐名_去除合并产品.apply(return_product1)
    #套餐后缀产品数量更换数据类型
    shell_data['产品数量'] =  shell_data['产品数量'].astype("int")
    #转换数据类型方便做合并
    shell_data['购买数量'] =  shell_data['购买数量'].astype("int")

    shell_data["产品总数量"] = shell_data.apply(lambda x: x["产品数量"]*x["购买数量"],axis=1)

    #开始计算
    #先修改名字  不修改的话带括号的名字在计算的时候容易出错
    #shell_data = shell_data.rename(columns={'商家实收金额(元)':'买家实际支付金额'})

    #新增加一个方法主要是排除不发货的订单，把备注标记不发货的订单的有效快递修改为0
    def return_KD_type(c):
        if(str(c).find("不发货") != -1):
            return 0
        else:
            return 1
    #开始修改有效快递属性
    shell_data['有效快递'] = shell_data.主订单备注.apply(return_KD_type)

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
    
    #总共销量表格加入type区分干预，真实，网站放单
    shell_data['type'] = shell_data.主订单备注.apply(return_type)
    #在df表里边加入各种销量数据
    v_shell_data = shell_data[shell_data['type']==1]
    g_shell_data = shell_data[shell_data['type']==2]
    t_shell_data = shell_data[shell_data['type']==0]
    df['销量'] = df.产品ID.apply(lambda x : t_shell_data.买家实际支付金额.loc[t_shell_data.商品id == x].sum())
    df['干预'] = df.产品ID.apply(lambda x : g_shell_data.买家实际支付金额.loc[g_shell_data.商品id == x].sum())
    df['放单'] = df.产品ID.apply(lambda x : v_shell_data.买家实际支付金额.loc[v_shell_data.商品id == x].sum())
    df['快递数量'] = df.产品ID.apply(lambda x : shell_data.计数.loc[shell_data.商品id == x].sum())
    #先要筛选出真实的和放单的shell_data对象
    shell_data_v_t = shell_data[(shell_data['type']==1)|(shell_data['type']==0)]
    df['快递数量（放+真）'] = df.产品ID.apply(lambda x : shell_data_v_t.计数.loc[shell_data_v_t.商品id == x].sum())
    df['产品总数量'] = df.产品ID.apply(lambda x : shell_data.产品总数量.loc[shell_data.商品id == x].sum())
    df['产品总数量（放+真）'] = df.产品ID.apply(lambda x : shell_data_v_t.产品总数量.loc[shell_data_v_t.商品id == x].sum())
    df['有效快递'] = df.产品ID.apply(lambda x : shell_data.有效快递.loc[shell_data.商品id == x].sum())

    #加入全称数据可以不显示
    df['商品全称'] = df.产品简称.apply(find_product_full_name2)

    #判断是否包含产品明细这个文件
    cost = True
    if os.path.exists(""+man_URL+"产品明细.xlsx"):
        print("存在产品明细文件开始计算产品明细")
        #通过产品简称对应一下产品进货价格
        get_product_price_df = get_product_price_file()

        #链接两个df（通过产品简称加入价格选项）
        df = pd.merge(df, get_product_price_df, how='left', left_on='产品简称', right_on='产品简称2')

        #生成新的列
        df["成本价格*产品总数量（放+真）"] = df["成本价格"] * df["产品总数量（放+真）"]
    else:
        cost = False
        print("不存在产品明细")


    #shell_data.to_csv(""+man_URL+day_time('today')+"all.csv",index=False,encoding="utf-8-sig")

    shell_data.to_csv(""+man_URL+day_time('today')+"all.csv",index=False,encoding="utf-8-sig")

    return df,cost

#写出文件
def write_file2(df,cost):
    global man_URL
    if(cost):
        #调整列位置开始输出
        df = df[["店铺","产品简称","商品全称","姓名","产品ID","组","销量","干预","放单","产品总数量（放+真）","有效快递","成本价格*产品总数量（放+真）"]]
    else:
        df = df[["店铺","产品简称","商品全称","姓名","产品ID","组","销量","干预","放单","产品总数量（放+真）","有效快递"]]
    
    #df.to_csv(""+man_URL+day_time('today')+"result.csv",index=False,encoding="utf-8-sig",columns=['店铺','产品简称','商品全称','姓名','产品ID','组','销量','干预','放单','直通车'])
    df.to_csv(""+man_URL+day_time('today')+"result.csv",index=False,encoding="utf-8-sig")


#==========================================控制部分==========================================
#检测执行步骤到哪一步卡死了
def content():
    print("判断路径")
    get_file_folder()
    print("载入配置文件")
    df = read_config_xlsx_new()
    print("开始载入销量数据")
    shell_date = get_sell_date_to_pd()
    print("开始计算")
    df = compute_result(df,shell_date)
    print("开始生成结果")
    write_file2(df[0],df[1])
    print("结束了")
    os.system('pause')
    os.system("explorer.exe %s" % ""+man_URL+"")

#主函数
if __name__ == "__main__":
    content()