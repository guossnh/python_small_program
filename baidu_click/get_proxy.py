#-*- coding : utf-8 -*-

import read_config , sys , requests

def tryproxy():
    global all_use_ip , can_use_ip , bc_ip , bc_proxy
    all_use_ip = all_use_ip + 1
    data = ''
    with urllib.request.urlopen(read_config.value('get_ip_link')) as f:
        data = f.read().decode()
    proxy_handler = urllib.request.ProxyHandler({'https': data})
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    try:
        wocao = opener.open('https://baidu.com')#测试链接是否可用
        print("链接正确")
        if wocao.status == 200:
            can_use_ip = can_use_ip + 1
            datalist = data.split(":")
            print("代理查找完毕,开始 设置浏览器代理")
            bc_ip = datalist[0]
            bc_proxy = datalist[1]
            return True
            #setHttpsProxy(datalist[0],datalist[1])
        else:
            return False
    except:
        time.sleep(3)
        print("链接出错")
        return False
    print("总共检测ip为%s可用ip为%s"% (all_use_ip,can_use_ip))

def get_proxy():
    pass

def try_proxy(proxy):
    proxy = "http://"+proxy
    try:
        content = requests.get("https://baidu.com" , proxies = {"https": proxy})
        if content.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def main():
    print(try_proxy("119.10.72.34:80")) 

if __name__ == '__main__':
    sys.exit(int(main() or 0))