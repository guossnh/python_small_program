#这是一个整理发货信息的程序整理发货信息
#主要步骤  py读取头条订单csv文件获取对象信息。复制发货文件到桌面并且并且将对象写入发货文件。在屏幕打印发货信息

#下边是导包
import csv,xlwt,xlrd,os,fnmatch
from xlutils.copy import copy

#下边是系统变量
allList = []#这个用来存放所有的发货信息数据
allNumList = []#这个用来存放所有的发货信息数据
addressOrder = "C:\\Users\\Administrator\\Desktop\\查询订单.csv" #这个是桌面的查询订单文件的路径
addressExpressSourse = "D:\\git\\python_small_program\\touTiaoFaHuo\\import.xls"#这个是import源文件路径
addressExpress = "C:\\Users\\Administrator\\Desktop\\import.xls"#这个是生成import文件路径
desktoplink = "C:\\Users\\Administrator\\Desktop\\"
fahuoCsv = "C:\\Users\\Administrator\\Desktop\\批量发货.csv"
#下边是主要函数

def readcsv():#读取下载的头条订单信息
    global allList
    with open(addressOrder,"r",encoding='utf-8') as f:
        cavfile = csv.reader(f,)
        next(cavfile)
        for i in cavfile:
            dictcustomer = {'sellid':i[0],'name':i[8],'address':i[10],'phone':i[9],'money':i[5],} 
            allList.append(dictcustomer)
    
def writexls():#写入发货上传的文件
    global allList
    #这个也需要try  catch
    r_xls = xlrd.open_workbook(addressExpressSourse,formatting_info=True) 
    w_xls = copy(r_xls) 
    sheet_write = w_xls.get_sheet(0)
    rownum = 3
    for values in allList:#023579.12.15.17.18.19
        sheet_write.write(rownum,0,values.get('sellid'))
        sheet_write.write(rownum,2,values.get('name'))
        sheet_write.write(rownum,3,values.get('phone'))
        sheet_write.write(rownum,5,values.get('address'))
        sheet_write.write(rownum,7,'日用品')
        sheet_write.write(rownum,9,1)
        sheet_write.write(rownum,12,'特惠送')
        sheet_write.write(rownum,15,'否')
        sheet_write.write(rownum,17,'否')
        sheet_write.write(rownum,18,'是')
        sheet_write.write(rownum,19,values.get('money'))
        if str(values.get('money'))=='98' or str(values.get('money'))=='108':
            sheet_write.write(rownum,23,'ZT*1+ZYK*10')
        elif str(values.get('money'))=='138':
            sheet_write.write(rownum,23,'ZT*2+ZYK*20')
        elif str(values.get('money'))=='168':
            sheet_write.write(rownum,23,'ZT*3+ZYK*30')
        elif str(values.get('money'))=='188':
            sheet_write.write(rownum,23,'ZT*4+ZYK*40')
        else:
            sheet_write.write(rownum,23,'价格出错请重新调整')
        rownum = rownum + 1 #添加下一行的数据d
    w_xls.save(addressExpress)

def readxlsx():
    global desktoplink,allNumList
    WaybillList = ""
    for file in os.listdir(desktoplink):
        if file.find("运单信息")!=-1:
            WaybillList = desktoplink + file
        else:
            pass
    if WaybillList !="":
        WaybillList.replace('\\','\\\\')#生成用于读取的文件
        try:
            workbook = xlrd.open_workbook(WaybillList)
            booksheet = workbook.sheet_by_index(0)
            for a in range(1,booksheet.nrows):
                #print(booksheet.cell_value(a,0))
                #print(booksheet.cell_value(a,1))
                fahuo = {"dingdanhao":booksheet.cell_value(a,0),"yundanhao":booksheet.cell_value(a,1),}
                allNumList.append(fahuo)
        except:
            print("读取运单信息文件时出错")
    else:
        print("桌面上边没有找到运单信息文件，请先下载文件在生成发货文件")

def docsv():#生成鲁班发货文件
    global fahuoCsv,allNumList
    with open(fahuoCsv,"w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        for value in allNumList:
            writer.writerow([value.get("dingdanhao"),"jd",value.get("yundanhao"),"河南省栾川县城关镇南大街46号"])
    

if __name__=="__main__":#主函数
    #while True:
    print('''
    输入 1 回车制作京东物流发货表单（桌面上必须有鲁班下载的查询订单.csv）
    输入 2 回车制作鲁班发货表单（桌面上必须有京东下载的'运单信息XXXXXXXXXX.xlsx'文件且只有一个否则会直接读取第一个文件）
    输入其他的值就退出
    ''')
    a = input()
    if a=='1':
        try:
            readcsv()
            try:
                os.remove(addressOrder)
                print("成功删除桌面上的查询订单.csv，这个文件已经没用了")
            except EnvironmentError:
                print("没有删除桌面上的查询订单.csv，这个文件已经被打开，请自己删除")
            writexls()
            print("总共收入"+str(len(allList))+"条订单信息，检查一下是否正确。不正确的话就不要使用了")
        except Exception:
            print("读取文件出错请确认桌面时候出现鲁班下载的查询订单.csv文件")
    elif a=='2':
        readxlsx()
        print("总共统计"+str(len(allNumList))+"条发货信息，检查一下是否正确。不正确的话就不要使用了")
        docsv()
        print("已经生成批量发货.csv  在你的桌面上边")
    else:
        pass