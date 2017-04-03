#-*- coding : utf-8 -*-
#这是读取 配置 文件 然后 返回 字典数据  修改一下
import json ,sys ,random
config = 'config.json'
config_var = ''
#传入key返回value   这个方法 好像 很没用啊
def value(key):
    return main()[key]

#返回json对象需要什么点什么
def main():
    global config , config_var
    with open(config,'r', encoding="utf8") as f:
        config_var = json.load(f)
    #return config_var#为了测试 先注释
    get_usergent()

def r_no_click():#这个是读取不点击链接的json文件,比较单一放这里试一下
    with open('no_click.json' , 'r' , encoding="utf8") as f:
        data = json.load(f)
        return data['js']
        #for x in data['js']:
        #    driver.execute_script(x,"")

def get_usergent():
    #这是一个随机获取浏览器UserAgent的方法,调用之后返回一个UserAgent的字符串
    with open('browser.json', 'r', encoding="utf8") as f:
        date = json.load(f)
    return list(date['phone_browser'].values())[int(random.uniform(0, len(date['phone_browser'])))]

if __name__ == '__main__':
    sys.exit(int(main() or 0))