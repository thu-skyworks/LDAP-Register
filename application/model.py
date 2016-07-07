import ldap
import logging
from helper import ErrorCode
import crypt
import base64
import bcrypt

from . import app

def passwd_hash(pwd):
    return '{CRYPT}'+crypt.crypt(pwd,'$6$'+bcrypt.gensalt()[0:7])

def obtain_handle():
    l = ldap.initialize('ldap://server2.thu-skyworks.org')
    l.bind_s(app.config['LDAP_BIND'], app.config['LDAP_BIND_PWD'], ldap.AUTH_SIMPLE)
    return l

def search_existing_user(handle, userid):
    res = handle.search_s(app.config['LDAP_BASE'],ldap.SCOPE_SUBTREE,'(cn={})'.format(userid),['cn','mail'])
    print res
    return len(res)>0

def search_existing_email(handle, email):
    res = handle.search_s(app.config['LDAP_BASE'],ldap.SCOPE_SUBTREE,'(mail={})'.format(email),['cn','mail'])
    print res
    return len(res)>0

def do_user_reg(userid, passwd, realname, email):
    try:
        l = obtain_handle()
        userid = userid.encode('utf-8')
        email = email.encode('utf-8')
        passwd = passwd_hash(passwd)
        if search_existing_user(l, userid):
            return ErrorCode.ALREADY_EXISTS
        if search_existing_email(l, email):
            return ErrorCode.ALREADY_EXISTS
        user_tpl={
            'objectClass': ('top','person','organizationalPerson','inetOrgPerson','extensibleObject'),
            'uid': userid,
            'displayName': userid,
            'authAuthority': ';basic;',
            'userPassword': passwd,
            'mail': email,
            'cn': userid,
            'sn': userid,
            'gecos': realname.encode('utf-8'),
            # mobile: 12333333333
            uidNumber: 1999999,
            gidNumber: 1000001,
            loginShell: '/bin/sh',
            homeDirectory: '/home/'+userid
        }
        attributes=[ (k,v) for k,v in user_tpl.items() ]
        l.add_s('uid={},'.format(userid)+app.config['LDAP_BASE'], attributes)
    except ldap.LDAPError, error:
        logging.error(error)
    except Exception, e:
        logging.exception(e)
