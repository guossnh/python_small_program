#-*- coding : utf-8 -*-
import pandas as pd
import os,time,csv



desktop_link = "C:\\Users\\Administrator\\Desktop\\"



#根据传入的参数分析这个条目是微信刷单网站放单还是真实销售
def remark_analysis(remark):
    remark = remark.split(";")[-1]#先要清洗一下remark
    if(remark.find("G-") or remark.find("g-")):
        return("微信刷单") 
    elif(remark.find("V-") or remark.find("v-")):
        return("网站放单刷单") 
    else:
        return("zhe last")






if __name__ == "__main__":
    remark_analysis("G-WZ;GWZ-111;GWZ-222")
    remark_analysis("G-WZ;GWZ-111；GWZ-222")
    remark_analysis("GWZ-111；GWZ-222")