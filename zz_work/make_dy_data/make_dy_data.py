#!/usr/bin/python
#-*- coding : utf-8 -*-

#这个程序就是郑州用于抖音计算的程序

import pandas as pd
import glob,os,openpyxl,re,platform,datetime
import urllib.request  

man_URL = "d:\\应用\\zzceshi1\\"


#======================通用方法======================
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

#这些是拆分字符串之后用来分裂的方法
def return_product0(z):
    try:
        z = z.split("-")[0]
        return z
    except:
        return "后台没写套餐编码"
def return_product1(z):
    try:
        z = re.split("-")[1]
        return z
    except:
        return 1

#订单类型判断
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


#======================计算方法======================

#下边三部分是读取三部分文件
#读取抖音销量文件放在一块不需要筛选时间
def get_sell_date_to_pd():
    #获取程序文件夹里边的需要统计的所有文件的数据
    def get_file_name_list():
        return glob.glob(r''+man_URL+'file\\*.csv')
    product_file_list = []
    print("读取"+str(len(get_file_name_list()))+"个销量数据文件")
    #放入list
    for product_file in get_file_name_list():
        try:
            product_file_list.append(pd.read_csv(product_file))
        except:
            print("数据文件"+product_file+"出现错误")
    #返回合并
    return pd.concat(product_file_list)

#读取读取并且合并多个快卖下载的文件
def add_km_file_for_code():

    #读取相应文件夹下边的所有xls格式文件
    def get_file_name_list(last_name):
        return glob.glob(r''+man_URL+'km\\*.'+last_name+'')

    print("开始读取快卖数据")
    xl_list = get_file_name_list("csv")
    gjp_list = []
    for x in xl_list:
        try:
            gjp_list.append(pd.read_csv(x,skiprows=6,encoding='GB18030'))
        except:
            print("读取快卖文件"+x+"出现错误")
    shell_gjp_data = pd.concat(gjp_list)
    shell_gjp_data = shell_gjp_data[["商品商家编码","商品名称"]]
    return shell_gjp_data

#读取姓名组ID数据并且返回数据文件
def read_name_data():
    global man_URL
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



#这里是整个数据的计算过程
def do_data(km_data,shell_data,p_data):
    #首先是shell_data的去除无关数据
    shell_data = shell_data[["子订单编号","商品数量","商品ID","商家编码","订单应付金额","订单状态","商家备注","买家留言","售后状态","订单提交时间"]]

    #筛选表格订单状态和售后状态
    shell_data = shell_data[(shell_data["订单状态"]=="已完成")|(shell_data["订单状态"]=="已发货")|(shell_data["订单状态"]=="待发货")]
    shell_data = shell_data[(shell_data["售后状态"]=="-")|(shell_data["售后状态"]=="售后关闭")]

    #是暂时需要修改一下因为商家编码更换了一次，往后彻底更换的话就可以注释掉下边的一句话
    shell_data['商家编码'] = shell_data['商家编码'].replace('QWZYLB-试用装','QWZYLBSYZ-1', regex=True)

    #分列
    shell_data['商家编码'] = shell_data['商家编码'].replace(r'\r+|\n+|\t+','', regex=True)
    shell_data['产品代码'] = shell_data.商家编码.apply(return_product0)
    shell_data['产品代码对应数量'] = shell_data.商家编码.apply(return_product1)
    shell_data['产品代码对应数量'] =  shell_data['产品代码对应数量'].astype("int")
    shell_data['type'] = shell_data.apply(lambda row: return_type(row['商家备注']),axis=1)

    #增加一列方便统计数量
    shell_data["订单量"] = 1

    #融合三个表并且根据商品ID去重
    #首先是shell_data 和 p_data
    #转换数据类型防止出错
    shell_data['商品ID'] = shell_data['商品ID'].astype(str).str.extract(r'(\d+)')
    p_data['产品ID'] = p_data['产品ID'].astype(str).str.extract(r'(\d+)')

    #先清理姓名表重复数据再合并
    p_data = p_data.drop_duplicates("产品ID")
    #用姓名表格链接 产品表格然后就可以了
    shell_data = pd.merge(shell_data, p_data, how='left', left_on='商品ID', right_on='产品ID')


    #然后是shell_data和km_data的合并
    shell_data = pd.merge(shell_data, km_data, how='left', left_on='产品代码', right_on='商品商家编码')

    #输出全文件，用来检查问题
    shell_data.to_csv(""+man_URL+"原始数据.csv",encoding="utf-8-sig")#生成原始数据方便差错纠错

    #返回数据包
    return shell_data

#写出文件
def write_file(new_shell_data):
    new_shell_data["订单应付金额"] = new_shell_data["订单应付金额"].astype("float64")

    #个人销售情况
    df1 = new_shell_data.pivot_table(index=["姓名"],values=["订单应付金额"],aggfunc = 'sum')
    
    #组销售情况
    df2 = new_shell_data.pivot_table(index=["组"],values=["订单应付金额"],aggfunc = 'sum')
    
    #店铺销售情况
    df3 = new_shell_data.pivot_table(index=["店铺"],values = ["订单应付金额"],aggfunc = 'sum',fill_value=0,margins=1)

    #产品销售情况
    df4 = new_shell_data.pivot_table(index=["商品名称"],values = ["订单应付金额","订单量"],aggfunc = 'sum',fill_value=0,margins=1)

    #外加 ~~~看看能不能统计出销售单品的数量
    with pd.ExcelWriter(r''+man_URL+'结果数据.xlsx') as writer:
        df1.to_excel(writer, sheet_name='个人销售情况',merge_cells=False)
        df2.to_excel(writer, sheet_name='组销售情况',merge_cells=False)
        df3.to_excel(writer, sheet_name='店铺销售情况',merge_cells=False)
        df4.to_excel(writer, sheet_name='产品销售情况',merge_cells=False)

#======================华丽的分割线======================

if __name__ == "__main__":
    if(kaiguan2()):
        print("访问正常")
        #开始判断修改操作区路径
        get_file_folder()
        #读取快卖数据获取产品信息和产品简称用于做对称
        km_data = add_km_file_for_code()
        #读取抖音下载数据
        shell_data = get_sell_date_to_pd()
        #读取抖音商品ID对应表
        p_data = read_name_data()
        #开始计算数据
        new_shell_data = do_data(km_data,shell_data,p_data)
        #生成需要的结果文件
        write_file(new_shell_data)

    else:
        print("无法获取配置文件")
