#coding: utf-8
import path
import glob
import os
import sys
import bottle

app = bottle.Bottle()
app.mp4list = []

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/img/<file_name>')
def img(file_name):
    return bottle.static_file(file_name, root=path.www+'/img')

@app.route('/css/<file_name>')
def css(file_name):
    return bottle.static_file(file_name, root=path.www+'/css')

@app.route('/js/<file_name>')
def js(file_name):
    return bottle.static_file(file_name, root=path.www+'/js')

@app.route('/fonts/<file_name>')
def fonts(file_name):
    return bottle.static_file(file_name, root=path.www+'/fonts')

class MP4:
    def __init__(self):
        self.fullpath = None
        self.name = None

def update_mp4list():
    fse = sys.getfilesystemencoding()
    files = [unicode(x, fse) for x in glob.glob(os.path.join(path.mp4, '*.mp4'))]
    new_list = []
    for file in files:
        mp4 = MP4()
        mp4.name = os.path.basename(file).lstrip('0123456789-').rstrip('.mp4')
        mp4.fullpath = file
        new_list.append(mp4)
    del app.mp4list
    app.mp4list = new_list

@app.route('/index')
def index():
    update_mp4list()
    return bottle.template('index', problem_list=[], mp4list=app.mp4list)

bottle.run(app, host='localhost', port=8888, debug=True)
