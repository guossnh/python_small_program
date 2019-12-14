#-*- coding : utf-8 -*-


import xlwt,xlrd,os,time

tuikuanNum = 0
MoneyAll = 0

xlsxonefile = "C:\\Users\\Administrator\\Desktop\\1.xlsx"

def dodate():
    content = '北京欢迎你为你开天辟地…………'
    while True:
        # 清理屏幕上的输出
        os.system('cls')  # os.system('clear')
        print(content)
        # 休眠200毫秒
        time.sleep(0.2)
        content = content[1:] + content[0]

dodate()