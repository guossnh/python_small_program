#-*- coding : utf-8 -*-
#这个是一个通过合并csv的程序，帮助会计合并csv文件


import pandas,os,time
from flask import Flask,request
from flask import render_template
from werkzeug.utils import secure_filename
import webbrowser

app = Flask(__name__)
UPLOAD_FOLDER = '/templates/upload'

@app.route('/', methods=['GET', 'POST'])
def home(name=None):
    return render_template('index.html', name=name)

@app.route('/upload',methods=[ 'POST'])
def get_file():
    if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      
      return 'file uploaded successfully'
    else:
        return "wocao"


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run()
