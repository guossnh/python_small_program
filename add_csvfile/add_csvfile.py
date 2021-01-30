#-*- coding : utf-8 -*-
#这个是一个通过合并csv的程序，帮助会计合并csv文件


import pandas,os,time
from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home(name=None):
    return render_template('index.html', name=name)

def man():
    pass

if __name__ == "__main__":
    app.run()
