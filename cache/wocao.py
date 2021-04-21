import pandas as pd
import glob,os
import urllib.request   

man_URL = "d:\\应用\\ceshi\\"

 
#这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name):
    return glob.glob(r''+man_URL+'*.'+last_name+'')


lists = get_file_name_list("csv")
data_list = []
for x in lists:
    try:
        data_list.append(pd.read_csv(x))
    except:
        print("读取"+x+"出现错误")

data_list = pd.concat(data_list)

data_list = data_list[(data_list["售后状态"]=="无售后或售后取消")|(data_list["售后状态"]=="售后处理中")]

data_list = data_list[(data_list["订单状态"]=="待发货")|(data_list["订单状态"]=="已发货，待签收")|(data_list["订单状态"]=="已签收")]

product_list = pd.read_csv("d:\\应用\\data.csv",encoding="gbk")

product_list = product_list[["产品ID","产品全称"]]

data_list = pd.merge(data_list, product_list, how='left', left_on='商品id', right_on='产品ID')

data_list = data_list[data_list["产品全称"]=="蝎毒追风贴"]


lists2 = get_file_name_list("xlsx")
data_list2 = []
for a in lists2:
    try:
        data_list2.append(pd.read_excel(a))
    except:
        print("读取"+a+"出现错误")

data_list2 = pd.concat(data_list2)

data_list2["订单号"] = data_list2["订单号"].astype(str)
data_list2["订单号"] = data_list2["订单号"].map(lambda x: str(x).lstrip('\t').rstrip('\t')).astype(str)
#data_list2["订单编号"] = data_list2["订单编号"].map(lambda x: str(x).lstrip('').rstrip('')).astype(str)
print(data_list2)

data_list = pd.merge(data_list, data_list2, how='left', on='订单号')

print(data_list)
data_list.to_csv(""+man_URL+"111.csv")
