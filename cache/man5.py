#-*- coding : utf-8 -*-
import  pandas as pd

data = pd.read_csv("C:\\Users\\Administrator\\Desktop\\all.csv",encoding="utf8")
#data2 = pd.read_csv("C:\\Users\\Administrator\\Desktop\\all.csv", encoding="gbk",delimiter="\t")
#df = pd.merge(data3, data2, how='left', on='phone')
#data.to_csv('C:\\Users\\Administrator\\Desktop\\result3.csv',index=False)
#print(data.duplicated(subset = ['phone'],keep="last"))
#newdata  = data.drop_duplicates(['phone'],keep="last")
#new1  = data.drop(data.index[179242:216060])
#new1 = new1.drop(['n1'],axis=1)
#new2 = data.drop(data.index[0:179241])
#new2 = new2.drop(['n2'],axis=1)
#new1.to_csv('C:\\Users\\Administrator\\Desktop\\result1.csv',index=False)
#new2.to_csv('C:\\Users\\Administrator\\Desktop\\result2.csv',index=False)
#newdata.to_csv('C:\\Users\\Administrator\\Desktop\\result3.csv',index=False)
#new1 = data.drop(data.index[179242:237642])
#new1 = new1.drop(['n1'],axis=1)
#new1.to_csv('C:\\Users\\Administrator\\Desktop\\result1.csv',index=False)
new2 = data.drop(data.index[0:179242])

new2.to_csv('C:\\Users\\Administrator\\Desktop\\result1.csv',index=False)