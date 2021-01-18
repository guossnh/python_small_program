#-*- coding : utf-8 -*-
#想做一个python自动获取多推吧数据的爬虫这样的话往后就不需要备注了 




def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.newContext()

    # Open new page
    page = context.newPage()

    page.goto("https://www.baidu.com/")

    page.click("input[name=\"wd\"]")

    page.fill("input[name=\"wd\"]", "jingdong")

    page.click("text=\"京东\"")

    # Click //a[normalize-space(.)='京东JD.COM官网 多快好省 只为品质生活']
    with page.expect_navigation():
        with page.expect_popup() as popup_info:
            page.click("//a[normalize-space(.)='京东JD.COM官网 多快好省 只为品质生活']")
        page1 = popup_info.value
    # ---------------------
    context.close()
    browser.close()

def man():
    pass


if __name__ == "__main__":
    man()