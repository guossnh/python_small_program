#-*- coding : utf-8 -*-

import  sys , requests ,urllib , time , read_config

def get(): #get proxy  
    data = '' #这是放获取的内容的变量
    print("wocao")
    with urllib.request.urlopen(read_config.value('get_ip_link')) as f:
        data  = f.read().decode()
    #if try_proxy(data):
    #    return data
    #else:
    #    time.sleep(3)
    #    return False
    #
    #    get()  #这样调用使用移动的网络容易 出现问题  狗日的移动
    while try_proxy(data):
        get()
    return data

def try_proxy(proxy):  #测试传过来的代理是否可用,这个会比之前 的办法好了
    proxy = "http://"+proxy
    try:
        content = requests.get("https://icanhazip.com/" , proxies = {"https": proxy})
        if content.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def main():
    pass

if __name__ == '__main__':
    sys.exit(int(main() or 0))