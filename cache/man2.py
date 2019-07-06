#-*- coding : utf-8 -*-


import xlwt,xlrd

tuikuanNum = 0
MoneyAll = 0

xlsxonefile = "C:\\Users\\Administrator\\Desktop\\1.xlsx"

def dodate():
    global tuikuanNum,MoneyAll
    workbook = xlrd.open_workbook(xlsxonefile)
    booksheet = workbook.sheet_by_index(0)
    #print(booksheet.cell_value(1,9))
    #print(type(booksheet.cell_value(1,9)))
    for a in range(1,booksheet.nrows):
        #print(booksheet.cell_value(9,0))
        if(booksheet.cell_value(a,9)=="退款成功"):
            tuikuanNum = tuikuanNum + 1
            continue
        elif(booksheet.cell_value(a,8)[0:4]=="FWJ-"):
            MoneyAll = MoneyAll + float(booksheet.cell_value(a,3))
        else:
            pass
    print(MoneyAll)
dodate()