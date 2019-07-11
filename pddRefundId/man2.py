#-*- coding : utf-8 -*-
#帮助秀云姨筛选出需要的id的标题
import os,re,csv
import urllib.request


csvFloder = 'C:\\csvdata\\'
fielread  = ''
fielwrite  = ''
csvDataList = []
resultHeaders = ['商户订单号','producttitle','productremark','发生时间','收入金额（+元）','支出金额（-元）','账务类型,备注']

def kaiguan():
    req = urllib.request.Request('http://1.guowenzhuo.sinaapp.com/taobao/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False



def findProductName(pddid):
    global fielread
    ruturnValue = '没有找到'
    remarkValue = '没有找到'
    pddid = str(pddid)
    with open(fielread,'rt',encoding='utf8') as f:
        readers = csv.reader(f)
        for line in readers:
            if(pddid==str(line[1])):
                ruturnValue = line[0]
                remarkValue = line[38]
                break
    return([ruturnValue,remarkValue])


def doFile():
    #这个方法操作两个文件填写需要的标题
    global fielwrite,csvDataList,resultHeaders
    onecsvDataList = []
    with open(fielwrite,'r+') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            if(row==[]):
                continue
            elif(re.match(r'\d{6}-\d+',row[0])):
                onecsvDataList = row
                getvalue = findProductName(row[0])
                onecsvDataList.insert(1,getvalue[1])
                onecsvDataList.insert(1,getvalue[0])
                csvDataList.append(onecsvDataList)
            else:
                print("wrong")
    with open(""+csvFloder+"result.csv",'a',newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(resultHeaders)
        f_csv.writerows(csvDataList)

def findFileRight():
    #这个方法判断文件夹是否存在两个csv文件并且两个csv文件是否正确.
    #获取需要读和写的的文件路径
    #返回真进行下一步的操作
    global fielread,csvFloder,fielwrite
    for file in os.listdir(csvFloder):
        if ((file.find("csv")!=-1)&(file.find("pdd")==-1)):
            fielread = csvFloder + file
        elif((file.find("csv")!=-1)&(file.find("pdd")!=-1)):
            fielwrite = csvFloder + file
    if((fielread=='')|(fielwrite=='')):
        print("没有找到文件你是否吧文件放入指定的文件夹并且解压")
        return False
    else:
        print("找到文件了开始下一步的操作")
        return True


if __name__ == "__main__":
    if(kaiguan()):
        if(findFileRight()):
            doFile()
            print("已经成功生成文件。不谢")
            kaiguan()
        else:
            pass