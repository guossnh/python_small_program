#下边是数据包
import urllib.request
import urllib.parse
import json , csv ,datetime

#下边的是变量
idlist =['3306395126959591900','3311636679286223197','3329665021532852507']#这是需要检测的数据id

urlHeader = 'https://haohuo.snssdk.com/product/ajaxstaticitem?id='
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#下边是方法
def getdata():
    global idlist,urlHeader,headers
    for sellid in idlist:
        request = urllib.request.Request(url = urlHeader+sellid,headers = headers)
        response = urllib.request.urlopen(request)
        sell_num = json.loads(response.read().decode('utf-8'))
        writeCsv([{'id':str("'"+sellid), 'name':sell_num.get("data").get("name"), 'sell_num':sell_num.get("data").get("sell_num"),'time':datetime.datetime.now(), }])

def writeCsv(row):#传入字典数据写入csv文件
    header = ['id','name','sell_num','time']
    with open('d:\\lixinwuData\\data.csv','a+',newline='') as f:
        f_csv = csv.DictWriter(f, header)
        #f_csv.writeheader()//不要重复写入表头
        f_csv.writerows(row)
    f.close

getdata()
