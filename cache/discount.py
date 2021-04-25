#!/usr/bin/python
#-*- coding : utf-8 -*-
#主要是计算拼多多如果设置最低价格 那么 打折和优惠券怎么样才能够一样呢
#价格范围 主要是100以内做低价的一般价格都是小数点之后两位那么我设置价格10000就用整数就可以了

paice = range(1,10001)
zhekou = range(1,100)

def zhekou_compute(x,y):
    return x * y *0.01

def yn_youhuiquan(z):
    if(z%100==0):
        return True
    else:
        return False

def man():
    for a in paice:
        for b in zhekou:
            if(yn_youhuiquan(a - zhekou_compute(a,b))):#筛选不是整数的优惠券
                if(zhekou_compute(a,b)*0.01>5):#筛选折扣价格之后价格小于5元的
                    if((a-zhekou_compute(a,b))*0.01<30.00):#筛选优惠券小于30元的
                        print("价格："+str(a*0.01)+"打"+str(b)+"折的价格是"+str(zhekou_compute(a,b)*0.01)+"   优惠券："+str((a-zhekou_compute(a,b))*0.01)+"")



if __name__ == "__main__":
    man()
