#-*- coding : utf-8 -*-

#这是导入包的过程
import requests,json

jsondata = ""

def getdate():
    global jsondata
    r = requests.get('https://Dre63QDX2ggUV4rK56TaeA:Wm0dn1MZjkt84UoQzOHd-g@jinshuju.net/api/v1/forms/eqbAZf/entries?Username=Dre63QDX2ggUV4rK56TaeA&Password=Wm0dn1MZjkt84UoQzOHd-g')
    jsondata = r.json()

def getdata():
    pass

if __name__ == "__main__":
    getdate()
    getdate()
