#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import pwd

server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
pd_config_file = os.path.join(server_dir, 'config.production.py')

if __name__ == '__main__':
    from application import app
    app.config.from_pyfile(config_file)

    #生产环境中覆盖某些配置选项
    if os.path.exists(pd_config_file):
        app.config.from_pyfile(pd_config_file)

    logging.basicConfig(filename = app.config['LOG_FILENAME'],  
        level = (logging.NOTSET if app.config['DEBUG'] else logging.INFO), format = '%(asctime)s [%(funcName)s][%(levelname)s]: %(message)s')  

    if app.config['DEBUG']:
        app.run()
    else:
        uid = pwd.getpwnam(app.config['WORKER_USER'])[2]
        os.setuid(uid)
        from flup.server.fcgi import WSGIServer
        WSGIServer(app, bindAddress=app.config['FASTCGI_SOCK']).run()