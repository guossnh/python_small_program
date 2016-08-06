#-*- coding : utf-8 -*-
#由于 百度 的限制 上传 文件 数量  不大于  1000的话  就是 每一个文件 夹  存储   999张  照片  这是 处理 文件 的程序
#另   你妹 的百度网盘  限制  真尼玛多

#导包
import os,sqlite3,shutil,zipfile





#变量
conn = sqlite3.connect('jiandan.db')#数据库初始化


#程序部分

#获取总共的信息条目
def get_all_num_db():
    global conn
    c = conn.cursor()
    c.execute("select count(*) from jiandan ")
    data=c.fetchone()
    return data[0]


#生成46个文件夹用于储存图片
def make_dic():
    for x in range(46):
        os.mkdir("f:\\jiandan_meizi\\%s"%(x))



#移动图片
def move_img():
    for x in range(1, get_all_num_db() + 1):
        try:
            shutil.move("f:\\jiandan_meizi\\%s"%(find_img_name(x)),"f:\\jiandan_meizi\\%s\\"%(int(x/1000)))
            prnt("ok one")
        except:
            print("move wrong")
        



#从数据库查文件名根据rowid
def find_img_name(rowid):
    global conn
    try:
        c = conn.cursor()
        c.execute("select link from jiandan where rowid = %s"%(rowid))
        data=c.fetchone()
    except:
        print("db select wrong")
    return data[0].split("/")[-1]


#对文件夹 进行分类
def do_zip(dir_name):
    z = zipfile.ZipFile("f:\\jiandan_meizi\\%s.zip"%(dir_name), 'w')
    file_dir = "f:\\jiandan_meizi\\%s"%(dir_name)
    for x in os.listdir(file_dir):
        z.write(file_dir+os.sep+x)




def main():
    pass
    #move_img()
    for x in range(1,46):
        do_zip(x)
    


if __name__ == '__main__':
    main()