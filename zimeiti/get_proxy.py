#-*- coding : utf-8 -*-

import  sys , requests ,urllib , time

def get(): #get proxy  
    data = '' #这是放获取的内容的变量
    with urllib.request.urlopen(read_config.value('get_ip_link')) as f:
        data  = f.read().decode()
    if try_proxy(data):
        return data
    else:
        time.sleep(3)
        get()

def try_proxy(proxy):  #测试传过来的代理是否可用,这个会比之前 的办法好了
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
    #print(try_proxy("119.10.72.34:80"))
    #get_proxy()
    print("ok")

if __name__ == '__main__':
    sys.exit(int(main() or 0))