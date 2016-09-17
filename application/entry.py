import os
import json
from functools import wraps
from flask import render_template, request, redirect, url_for, send_from_directory
from flask import abort
from . import app
import views

#static files should be handled by 
#http server(e.g. nginx) in production environment
def handle_static(res, name):
    if not app.config['DEBUG']:
        abort(403)
        return
    return send_from_directory(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../static/'+res), name)

@app.route('/js/<path:name>')
def static_js(name):
    return handle_static('js',name)
@app.route('/css/<path:name>')
def static_css(name):
    return handle_static('css',name)
@app.route('/img/<path:name>')
def static_img(name):
    return handle_static('img',name)
@app.route('/favicon.ico')
def static_favicon():
    return handle_static('img','favicon.ico')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not views.check_login():
            return redirect('index')
        return f(*args, **kwargs)
    return decorated_function

_tpl_dir = os.path.dirname(os.path.realpath(__file__))+'/templates/'
def send_page(name):
    return send_from_directory(_tpl_dir, name)

@app.route('/')
@app.route('/index')
def page_index():
    return send_page('index.html')

@app.route('/user/reg', methods=['POST'])
def page_reg():
    return views.user_reg()

@app.route('/user/reset1', methods=['POST'])
def page_reset1():
    return views.user_reset_pwd_step1()

@app.route('/user/reset2', methods=['POST'])
def page_reset2():
    return views.user_reset_pwd_step2()

