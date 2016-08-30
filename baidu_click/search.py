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
def setHttpsProxy(ip,port,useragent = "",is_phone = False):#参数  ip地址   端口  这是useragent
    global driver , profile#全局变量
    profile = webdriver.FirefoxProfile(read_config.value("firfox_default_file"))
    try:
        profile.set_preference('network.proxy.type', 1)#设置浏览器上完方式为手动
        profile.set_preference('network.proxy.ssl', ip)#这里设置代理ip
        profile.set_preference('network.proxy.ssl_port', port)#这是设置代理的端口
        if useragent == "" :#判断usergaent是否为空
            profile.set_preference('general.useragent.override', useragent)#这是里设置useragent
        profile.update_preferences()
        driver = webdriver.Firefox(profile)#设置浏览器
        if is_phone:
            driver.set_window_size(450 , 800)#这是设置浏览器窗口的大小的地方
        else:
            driver.maximize_window()#浏览器最大化(这个可选)
        return True
    except:
        return False


#页面停留
def pageReader(times = 10, stoptimes = 3):
    global driver#全局变量
    time.sleep(3) #先休息3秒防止出错
    num = 180   #固定值是180根据百度搜多搜索页面高度1879
    for x in range(1,int(random.uniform(4,times))): #循环  设置循环表示要跳转几次. 上线 的话 可以多添加 几次
        time.sleep(3)   #每次循环之后 添加停留时间  增加容错率
        if suiji(5):
            num = num + 180
        else:
            num = abs(num - 180)
        #num = abs(num + int(random.sample([180,-180],1)))   #这种写法更吊  但是  出错  有时间看看 修改一下
        driver.execute_script("window.scrollBy(0,%s)" % num,"") #最后了  开始 跳转  就酱


#提供随机数  直接返回布尔值  默认为70%
def suiji(sum = 7):
    if int(random.uniform(0,10))<sum:
        return True
    else:
        return False


#百度搜索开始搜索方法
def baidustart(kew):
    global driver , kewword , baiduTitle #引入全局变量
    setHttpsProxy(bc_ip , bc_proxy)#设置浏览器的代理
    kewword = kew
    time.sleep(5)
    driver.get("https://www.baidu.com/s?wd="+kewword)#开始搜索关键字
    driver.maximize_window()#浏览器最大化(这个 可选)
    assert baiduTitle in driver.title#确定页面是百度搜索页面


def program_load():
    pass


def main():
    pass

if __name__ == '__main__':
    sys.exit(int(main() or 0))
