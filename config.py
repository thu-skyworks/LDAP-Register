import os.path as path

DEBUG = True
FASTCGI_SOCK = '/tmp/ldap_reg_web.sock'
WORKER_USER = 'zhang'

SECRET_KEY = 'key4development_env'

LOG_FILENAME  = path.join(path.dirname(path.realpath(__file__)),'app.log')

LDAP_BASE = ''
LDAP_BIND = ''
LDAP_BIND_PWD = ''

LDAP_UID_CONF = ''

GID_NUMBER = '1000001'