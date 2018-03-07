import webbrowser,time,os

#添加firfox
firefox_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)

urllist = ["http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557342@7","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347&seg=1@35","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347&seg=2@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347&seg=3@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347&seg=4@40","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557343@25","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557343&seg=1@43","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557343&seg=2@20","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557343&seg=3@8","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557343&seg=4@15","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557343&seg=5@17","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557344@6","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557344&seg=1@25","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557344&seg=2@29","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557345@3","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557346@7","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557346&seg=1@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557346&seg=2@20","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557346&seg=3@20","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557347@35","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557348@10","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557349@3","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557349&seg=1@4","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557349&seg=2@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557352@15","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557352&seg=1@10","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557352&seg=2@21","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557352&seg=3@7","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557350@5","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557350&seg=1@25","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557350&seg=2@30","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557351&seg=1@15","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557351&seg=2@15","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557351&seg=3@25","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557351&seg=4@50","http://i.yanxiu.com/uft/course/courseview.vm?trainingid=2803&courseid=10557341@110"]

def wocao (u,t):
    c = webbrowser.get('firefox')
    c.open(u,new=0)
    time.sleep(t*61)
    os.system("taskkill /F /IM FireFox.exe")

def main():
    global urllist
    for x in urllist:
        wocao(x.split('@')[0],int(x.split('@')[1]))


if __name__ == '__main__':
    main()

