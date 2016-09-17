#! /usr/bin/python
# -*- encoding: utf-8 -*-

import ldap, ldap.modlist
import requests
import logging
from helper import ErrorCode
import crypt
import base64
import bcrypt

from . import app, mail_helper, verification

def passwd_hash(pwd):
    return '{CRYPT}'+crypt.crypt(pwd,'$6$'+bcrypt.gensalt()[0:7])

def obtain_handle():
    l = ldap.initialize('ldap://server2.thu-skyworks.org')
    l.bind_s(app.config['LDAP_BIND'], app.config['LDAP_BIND_PWD'], ldap.AUTH_SIMPLE)
    return l

def search_existing_user(handle, userid):
    res = handle.search_s(app.config['LDAP_BASE'],ldap.SCOPE_SUBTREE,'(cn={})'.format(userid),['cn','mail'])
    logging.debug(res)
    return len(res)>0

def search_existing_email(handle, email):
    res = handle.search_s(app.config['LDAP_BASE'],ldap.SCOPE_SUBTREE,'(mail={})'.format(email),['cn','mail'])
    logging.debug(res)
    return len(res)>0

def next_uid_number(handle):
    uidNumber = None
    retries = 10
    while True:
        res = handle.search_s(app.config['LDAP_UID_CONF'],ldap.SCOPE_SUBTREE,'(objectClass=sambaUnixIdPool)',['uidNumber'])
        assert len(res)>0
        uidNumber = res[0][1]['uidNumber'][0]
        uidNumber = int(uidNumber)
        modlist = ldap.modlist.modifyModlist(
                {"uidNumber": [str(uidNumber)]}, 
                {"uidNumber": [str(uidNumber+1)]}
            )
        try:
            handle.modify_s(app.config['LDAP_UID_CONF'], modlist)
        except Exception, e:
            logging.info(e)
        else:
            break
        retries -= 1
        if retries <= 0:
            raise Exception('failed to increase uidNumber')

    return uidNumber

def do_passwd_reset_verify(email):
    try:
        l = obtain_handle()
        email = email.encode('utf-8')
        if not search_existing_email(l, email):
            return ErrorCode.NO_SUCH_USER
        verify = verification.alloc_verification_code({'op': 'reset_passwd', 'email': email})
        assert len(verify)>0
        link = app.config['SYS_MAIL_LINK_BASE']+'/#/reset?reset_step2&code='+verify
        mail_helper.send(app.config['SYS_MAIL_FROM'], email, app.config['SYS_MAIL_SUBJECT'], '密码重置', link)
        return ErrorCode.SUCCESS
    except ldap.LDAPError, error:
        logging.error(error)
    except Exception, e:
        logging.exception(e)
    return ErrorCode.UNKNOWN

def do_passwd_reset(verify, newpasswd):
    data = verification.check_verification_code(verify)
    logging.debug(data)
    if data is None or data['op']!='reset_passwd':
        return ErrorCode.INVALID_VERIFICATION
    return do_passwd_change(data['email'], newpasswd)

def do_passwd_change(email, newpasswd):
    try:
        l = obtain_handle()
        email = email.encode('utf-8')
        passwd = passwd_hash(newpasswd)

        res = l.search_s(app.config['LDAP_BASE'],ldap.SCOPE_SUBTREE,'(mail={})'.format(email),['cn','mail'])
        logging.debug(res)
        assert len(res)>0
        dn = res[0][0]
        logging.info('Modify password of {}'.format(dn))
        l.modify_s(dn, [( ldap.MOD_REPLACE, 'userPassword', passwd )])
        return ErrorCode.SUCCESS
    except ldap.LDAPError, error:
        logging.error(error)
    except Exception, e:
        logging.exception(e)
    return ErrorCode.UNKNOWN

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
        uidNumber = next_uid_number(l)
        logging.info('Next uidNumber is {}'.format(uidNumber))
        user_tpl={
            'objectClass': ('top','posixAccount','shadowAccount','person','organizationalPerson','inetOrgPerson','apple-user','extensibleObject'),
            'uid': userid,
            'displayName': userid,
            'authAuthority': ';basic;',
            'userPassword': passwd,
            'mail': email,
            'cn': userid,
            'sn': userid,
            'gecos': realname.encode('utf-8'),
            # mobile: 12333333333
            'uidNumber': str(uidNumber),
            'gidNumber': app.config['GID_NUMBER'],
            'loginShell': '/bin/sh',
            'homeDirectory': '/home/'+userid
        }
        attributes=[ (k,v) for k,v in user_tpl.items() ]
        logging.debug(attributes)
        l.add_s('uid={},'.format(userid)+app.config['LDAP_BASE'], attributes)
        logging.info('Registered')
        return ErrorCode.SUCCESS
    except ldap.LDAPError, error:
        logging.error(error)
    except Exception, e:
        logging.exception(e)
    return ErrorCode.UNKNOWN

def check_permisson(email):
    try:
        payload = {'subscriber': email, 'list_id': app.config['MAIL_LIST_PERM_CHECK']}
        r = requests.post(app.config['API_GET_MEMBER'], data=payload)
        logging.debug(r.text)
        j = r.json()
        if ('total_size' in j.keys()) and j['total_size'] > 0:
            return True
    except Exception, e:
        logging.exception(e)
    return False

