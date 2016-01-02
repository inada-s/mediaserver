#coding: utf-8
import path
import glob
import os
import sys
import bottle
import time
import datetime
import urllib2
import re
import urlparse

app = bottle.Bottle()
app.mp4list = []
app.mp4list_update = None

def cached_static_file(file_name, root):
    res = bottle.static_file(file_name, root=root)
    res.set_header("Cache-Control", "public, max-age=86400")
    return res

@app.route('/mediasv/img/<file_name>')
def img(file_name):
    return cached_static_file(file_name, root=path.www+'/img')

@app.route('/mediasv/css/<file_name>')
def css(file_name):
    return cached_static_file(file_name, root=path.www+'/css')

@app.route('/mediasv/js/<file_name>')
def js(file_name):
    return cached_static_file(file_name, root=path.www+'/js')

@app.route('/mediasv/fonts/<file_name>')
def fonts(file_name):
    return cached_static_file(file_name, root=path.www+'/fonts')

@app.route('/mediasv/thumb/<file_name>')
def thumb(file_name):
    return cached_static_file(file_name, root=path.thumb)

class MP4:
    def __init__(self):
        self.fullpath = None
        self.name = None
        self.playpath = None
        self.ctime = None
	self.size = None
	self.thumb = None

def update_mp4list():
    if app.mp4list_update and time.time() - app.mp4list_update < 60.0:
        return
    fse = sys.getfilesystemencoding()
    files = sorted(glob.glob(os.path.join(path.mp4, '*.mp4')), reverse=True)
    new_list = []
    for raw_name in files:
    	file = unicode(raw_name, fse)
        raw_file = os.path.basename(raw_name)
    	stat = os.stat(file)
	filename = os.path.basename(file)
        mp4 = MP4()
        mp4.name = os.path.splitext(filename.lstrip('0123456789-'))[0]
	mp4.playpath = urllib2.quote('/mediasv/play/' + raw_file)
        mp4.fullpath = file
	mp4.ctime = datetime.datetime.strptime(time.ctime(stat.st_ctime), "%a %b %d %H:%M:%S %Y")
	mp4.size = stat.st_size
	mp4.thumb = urllib2.quote('/mediasv/thumb/' + os.path.splitext(raw_file)[0] + '.jpg')
        new_list.append(mp4)
    del app.mp4list
    app.mp4list = new_list
    del app.mp4list_update
    app.mp4list_update = time.time()

def make_hardlink(src): 
    import ctypes 
    linkfile = str(time.time()) + '.mp4'
    dst = os.path.join(path.link, linkfile)
    command = 'mklink /h "%s" "%s"' % (dst, src)
    print command
    os.system(command)
    return linkfile

def delete_expired_hardlink():
    for link in glob.glob(os.path.join(path.link, '*.mp4')):
        filename = os.path.basename(link)
        dt = 0.0
        try:
	    dt = time.time() - float(os.path.splitext(filename)[0])
        except:
            pass
        if dt > 3600 * 24:
            os.system('del ' + link)

@app.route('/mediasv/play/<file_name>')
def play(file_name):
    fullpath = os.path.join(path.mp4, file_name)
    if not os.path.exists(fullpath):
        bottle.abort(404, 'Not Found.')
    delete_expired_hardlink()
    linkfile = make_hardlink(fullpath)
    bottle.redirect('/link/' + linkfile)

@app.route('/mediasv/index')
def index():
    update_mp4list()
    mp4list = app.mp4list
    page = 1
    search = ''
    search_query = ''
    if 'page' in bottle.request.query:
        try:
            v = int(bottle.request.params['page'])
            if v > 0:
                page = v
        except:
            pass
    if 'search' in bottle.request.query:
        try:
            search = bottle.request.query['search'].decode('utf-8')
            mp4list = filter((lambda x: re.search(search, x.name)), app.mp4list)
            search_query = '&search=' + urllib2.quote(bottle.request.query['search'])
        except:
            pass
    n = len(mp4list)
    begin = min(n, (page-1) * 20)
    end = min(n, begin + 20)
    return bottle.template('index', page=page, maxpage=n/20+1, mp4list=mp4list[begin:end], search=search, search_query=search_query)

bottle.run(app, host='localhost', port=8888, debug=True)
