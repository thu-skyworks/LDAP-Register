import re
import logging
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
        # if not userid or not passwd or not realname or not email:
        #     return empty_json_response(ErrorCode.WRONG_ARGUMENT)
        valid = re.match('^\w+$', userid) is not None
        if not valid:
            return empty_json_response(ErrorCode.WRONG_ARGUMENT)
        ret = model.do_user_reg(userid, passwd, realname, email)
      
        return json_response(ret, {})
    except Exception, e:
        logging.exception('Exception occurred')
    return empty_json_response(ErrorCode.WRONG_ARGUMENT)

