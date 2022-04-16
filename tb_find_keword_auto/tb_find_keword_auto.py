#-*- coding : utf-8 -*-
#这个程序准备筛选一组词 再淘宝搜索查询自然搜索之后天猫占比和基本销量

from time import time
from playwright.sync_api import sync_playwright


man_url = "d:\\应用\\try1\\"

#这个方法主要就是通过关键词调用浏览器 获取这个关键词的一般销量数据
def get_data_from_keword(playwright):
    # playwright.brwoser_type.action(**kwargs)可以理解为指定浏览器内核
    browser = playwright.chromium.launch_persistent_context(user_data_dir ="C:\\Users\\guoss\\AppData\\Local\\Google\\Chrome\\User Data\\Default",channel="chrome",headless=False,executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    # 根据浏览器内核创建浏览器
    
    #context = browser.new_context(accept_downloads=False)
    # 创建新页面
    page = browser.new_page()
    page.goto("https://taobao.com")

    page.fill('#q', '手机')

    page.click('.btn-search')

    page.wait_for_load_state()

    print(page.title())



    
    browser.close()


#通过返回的数据写入文件，每次执行的时候都先读取文件之后再开始执行
def w_file():
    pass

#读取文件然后判断从哪一个词开始搞
def r_file():
    pass

#主要操作方法
def content():
    #调用方法通过浏览器
    with sync_playwright() as playwright:
        get_data_from_keword(playwright)

#主函数
if __name__ == "__main__":
    content()