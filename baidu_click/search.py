#-*- coding : utf-8 -*-
#导入模块
#这是python模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time , random , string  , binascii , csv , json
#下边是自己的模块
import read_config

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
        if useragent != "" :#判断usergaent是否为空
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
    time.sleep(stoptimes*60)#页面停留时间默认3分钟,因为百度会根据时间判断页面的重要性
    num = 180   #固定值是180根据百度搜多搜索页面高度1879
    for x in range(1,int(random.uniform(4,times))): #循环  设置循环表示要跳转几次. 上线 的话 可以多添加 几次
        time.sleep(3)   #每次循环之后添加停留时间增加容错率
        if suiji(5):
            num = num + 180
        else:
            num = abs(num - 180)
        #num = abs(num + int(random.sample([180,-180],1)))   #这种写法更吊  但是  出错  有时间看看 修改一下
        driver.execute_script("window.scrollBy(0,%s)" % num,"") #最后了  开始 跳转  就酱


#这个页面 是百度 搜索 列表的阅读 页面   不知带 有用没  先 用用吧
def baidu_list_page_reader():
    global driver#全局变量
    time.sleep(5) #先休息5秒防止出错
    num = 180   #固定值是180根据百度搜多搜索页面高度1879
    #先要 跳转到 页面 最下边
    for x in xrange(1,11):
        driver.execute_script("window.scrollBy(0,%s)" %(x*num),"") #最后了  开始 跳转  就酱
    #之后开始 随机跳转
    pageReader(10,0.2)

#这个办法主要是 放一些 排除 的网站,然后  其他 的网站   都要 点击
#delete not click link use javascript on baidu.com list page
#at last add this to wile_be_start()
def noClick():
    with open('no_click.json' , 'r' , encoding="utf8") as f:
        data = json.load(f)
        for x in data['js']:
            driver.execute_script(x,"")

#这个方法主要实现的是跳转到百度下一页 的页面.时间 的话   可以 根据 电脑 适当 的调节
def baiduNextPage():
    global baiduTitle , driver
    time.sleep(5)#等待页面载入
    assert baiduTitle in driver.title#确定页面是百度搜索页面
    driver.implicitly_wait(10)#隐试等待
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")#滚动到最下边.没什么卵用
    driver.find_element_by_link_text("下一页>").click()


#下边是两套规则
#规则1  除了过滤器其他的 都点
def type1():
    time.sleep(5) #时间停留5秒 增加系统容错率
    i = 0
    while i<=baidupagenumber1:#这是翻页的循环
        i = i + 1
        time.sleep(3)
        noClick()#过滤掉不要的链接
        content_list_num = driver.find_elements_by_tag_name("h3")
        print("打印出  总共  有几个元素:%s"%len(content_list_num))
        for x in content_list_num:
            if suiji():
                #print("随机数打印到了")
                try:
                    x.find_element_by_tag_name("a").click()
                    time.sleep(5)
                    driver.switch_to_window(driver.window_handles[-1])
                    pageReader()
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
                    time.sleep(5)
                except:
                    print("错误一次")
            else:
                print("随机数没有打印到")
        baiduNextPage()
        print("结束.开始第二页")


#规则2  点击特定的页面   其他的不点
def type2(link):
    time.sleep(5) #时间停留5秒 增加系统容错率
    i = 0
    while i<=baidupagenumber2:#这是翻页的循环
        i= i + 1
        try:
            driver.find_element_by_partial_link_text(link).click()
            time.sleep(5)
            driver.switch_to_window(driver.window_handles[-1])
            pageReader()
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            time.sleep(5)
            print("找到链接,并且浏览成功")    
        except:
            print("没找到")
        baiduNextPage()
    print("结束.离开")

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

#这是页面载入的时候 开始 初始化 变量 的方法
def program_load():
    pass

#主要控制办法,接收参数开始执行一次搜索
def main(ip , port , kewword , type):
    pass

if __name__ == '__main__':
    sys.exit(int(main() or 0))
