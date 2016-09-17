import re
import logging
from validate_email import validate_email
from flask import request
from helper import empty_json_response, json_response, ErrorCode
import model

def user_reg():
    code = ErrorCode.UNKNOWN
    try:
        userid = request.form['userid']
        passwd = request.form['passwd']
        realname = request.form['realname']
        email = request.form['email']
        if not userid or not passwd or not realname or not email:
            return empty_json_response(ErrorCode.WRONG_ARGUMENT)
        valid = re.match('^\w+$', userid) is not None
        if not valid or not validate_email(email):
            return empty_json_response(ErrorCode.WRONG_ARGUMENT)
        if not model.check_permisson(email):
            return empty_json_response(ErrorCode.PERMISSION_DENIED)
        ret = model.do_user_reg(userid, passwd, realname, email)
      
        return json_response(ret, {})
    except Exception, e:
        logging.exception('Exception occurred')
    return empty_json_response(code)

def user_reset_pwd_step1():
    code = ErrorCode.UNKNOWN
    try:
        email = request.form['email']
        if not email or not validate_email(email):
            return empty_json_response(ErrorCode.WRONG_ARGUMENT)
        # if not model.check_permisson(email):
        #     return empty_json_response(ErrorCode.PERMISSION_DENIED)
        code = model.do_passwd_reset_verify(email)
        return empty_json_response(code)
    except Exception, e:
        logging.exception('Exception occurred')
    return empty_json_response(code)

def user_reset_pwd_step2():
    code = ErrorCode.UNKNOWN
    try:
        passwd = request.form['passwd']
        verify = request.form['code']
        if not passwd or not verify:
            return empty_json_response(ErrorCode.WRONG_ARGUMENT)
        code = model.do_passwd_reset(verify, passwd)
        return empty_json_response(code)
    except Exception, e:
        logging.exception('Exception occurred')
    return empty_json_response(code)
