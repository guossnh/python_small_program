#-*- coding : utf-8 -*-

#导入模块
#这是python模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time , random , string  , binascii , csv , json
#下边是自己的模块
import get_proxy , read_config

#这里是全局变量
driver = "" #这是浏览器对象

#这是初始化浏览器的办法
def setHttpsProxy(ip,port,useragent,is_phone = False):#参数  ip地址   端口  这是useragent
    global driver , profile#全局变量
    profile = webdriver.FirefoxProfile(profileDir)
    try:
        profile.set_preference('network.proxy.type', 1)#设置浏览器上完方式为手动
        profile.set_preference('general.useragent.override', "wocao")#这是里设置useragent
        profile.set_preference('network.proxy.ssl', ip)#这里设置代理ip
        profile.set_preference('network.proxy.ssl_port', port)#这是设置代理的端口
        profile.update_preferences()
        driver = webdriver.Firefox(profile)#设置浏览器
        if is_phone:
            driver.set_window_size(450 , 800)#这是设置浏览器窗口的大小的地方
        else:
            driver.maximize_window()#浏览器最大化(这个可选)
        return True
    except:
        return False






def main():
    pass

if __name__ == '__main__':
    sys.exit(int(main() or 0))
