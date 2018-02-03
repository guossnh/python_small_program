import webbrowser,time,os

#添加firfox
firefox_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)

urllist = ["http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557346@8","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557346&seg=1@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557346&seg=2@20","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557346&seg=3@20","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347@40","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347&seg=1@40","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347&seg=2@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347&seg=3@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347&seg=4@40","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557348@10","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557349@5","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557349&seg=1@5","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557349&seg=2@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557352@20","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557352&seg=1@11","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557352&seg=2@25","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557352&seg=3@10","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557350@5","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557350&seg=1@25","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557350&seg=2@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557351&seg=1@15","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557351&seg=2@15","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557351&seg=3@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557351&seg=4@45"]

def wocao (u,t):
    c = webbrowser.get('firefox')
    c.open(u,new=0)
    time.sleep(t*60)
    os.system("taskkill /F /IM FireFox.exe")

def main():
    global urllist
    for x in urllist:
        wocao(x.split('@')[0],int(x.split('@')[1]))


if __name__ == '__main__':
    main()

