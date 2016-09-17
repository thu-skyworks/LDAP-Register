import os.path as path

DEBUG = True
FASTCGI_SOCK = '/tmp/ldap_reg_web.sock'
WORKER_USER = 'zhang'

SECRET_KEY = 'key4development_env'

LOG_FILENAME  = path.join(path.dirname(path.realpath(__file__)),'app.log')

#LDAP base DN
LDAP_BASE = ''

#LDAP bind DN and password
LDAP_BIND = ''
LDAP_BIND_PWD = ''

#for uid autoincrement
LDAP_UID_CONF = ''

#default GID for user record
GID_NUMBER = '1000001'

#Mailman3 REST API url
API_GET_MEMBER = 'http://restadmin:restpass@localhost:8001/3.0/members/find'

#Mailing for authentication
MAIL_LIST_PERM_CHECK = 'notifications.groups.thu-skyworks.org'

#System mail configs
SMTP_SERVER = 'localhost:2525'
SYS_MAIL_FROM = 'no-reply@groups.thu-skyworks.org'
SYS_MAIL_SUBJECT = '天空工场账号服务'
SYS_MAIL_LINK_BASE = 'http://127.0.0.1:5000'

