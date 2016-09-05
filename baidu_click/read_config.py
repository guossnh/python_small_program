#-*- coding : utf-8 -*-
#这是读取 配置 文件 然后 返回 字典数据
import json ,sys 
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
    return config_var

def r_no_click():#这个是读取不点击链接的json文件,比较单一放这里试一下
    with open('no_click.json' , 'r' , encoding="utf8") as f:
        data = json.load(f)
        return data['js']
        #for x in data['js']:
        #    driver.execute_script(x,"")


if __name__ == '__main__':
    sys.exit(int(main() or 0))