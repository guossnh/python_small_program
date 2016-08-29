#-*- coding : utf-8 -*-

import get_proxy , time


def asd(abc):
    print(123)
    if abc:
        print("ok")
    else:
        print("else")
        asd(True)

#print(get_proxy.get())

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(time.sleep(3))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

