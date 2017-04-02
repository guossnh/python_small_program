#-*- coding : utf-8 -*-
'''这里不写东西就拉横线  真TM难看'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys ,get_proxy,time ,read_config,random

driver = "" #这是浏览器对象

profile = ""#设置浏览器基本设置

baiduTitle = ""#设置百度标题,用于判断是否页面已经载入


#这是初始化浏览器的办法
def setHttpsProxy(ip,port,useragent = ""):#参数  ip地址   端口  这是useragent
    global driver , profile#全局变量
    profile = webdriver.FirefoxProfile(read_config.value("firfox_default_file"))#使用本地的firfox的配置文件
    #profile.set_preference('network.proxy.type', 1)#设置浏览器上完方式为手动
    if ip !='':
        profile.set_preference('network.proxy.ssl', ip)#这里设置代理ip
        profile.set_preference('network.proxy.ssl_port', port)#这是设置代理的端口
    if useragent != "" :#判断usergaent是否为空
        profile.set_preference('general.useragent.override', useragent)#这是里设置useragent
    profile.update_preferences()
    driver = webdriver.Firefox(profile)#设置浏览器
    driver.maximize_window()#浏览器最大化(这个可选)


def pageReader(times = 10, stoptimes = 3):#页面停留
    global driver#全局变量
    time.sleep(stoptimes*read_config.value("page_stop_time"))#页面停留时间默认3分钟,因为百度会根据时间判断页面的重要性
    num = 180   #固定值是180根据百度搜多搜索页面高度1879
    for x in range(1,int(random.uniform(4,times))): #循环  设置循环表示要跳转几次. 上线 的话 可以多添加 几次
        time.sleep(3)   #每次循环之后添加停留时间增加容错率
        num = abs(num + int(random.sample([180,-180],1)[0]))
        driver.execute_script("window.scrollBy(0,%s)" % num,"") #最后了  开始 跳转  就酱



def main():
    '''主函数'''
    proxy = get_proxy.get()



if __name__ == '__main__':
    sys.exit(int(main() or 0))
    