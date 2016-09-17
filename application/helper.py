import json, base64, hashlib, random, string
import urllib
import urlparse
import httplib
import logging

class ErrorCode(object):
    """response error type"""
    UNKNOWN = -1
    SUCCESS = 0
    WRONG_ARGUMENT = 1
    NO_SUCH_USER = 2
    WRONG_PASSWD = 3
    NOT_LOGGED_IN = 4
    ALREADY_EXISTS = 5
    EXPIRED = 6
    NOT_BIND = 7
    NEED_OAUTH_AGAIN = 8
    NO_POSTS = 9
    FRIEND_NOT_REG = 10
    PASSWD_LEN = 11
    SNS_API_ERROR = 12
    API_TIMEOUT = 13
    QY_API_ERROR = 14
    ONLY_ONE_BIND = 15
    PERMISSION_DENIED = 16
    PARSE_TOPLIST_ERROR = 17
    IN_PROGRESS = 18
    INVALID_VERIFICATION = 19

def json_response(errorCode, data):
    return json.dumps({'error': errorCode, 'response': data})

def empty_json_response(errorCode):
    return json.dumps({'error': errorCode})

def hash_password(raw, salt):
    stage1 = base64.b64encode(raw + salt)
    m = hashlib.md5()
    m.update(stage1)
    m.update(salt)
    return m.hexdigest()

def rand_generator(size, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def update_params_in_url(url, params):

    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urllib.urlencode(query)

    return urlparse.urlunparse(url_parts)

def patch_httplib():
    
    old_send= httplib.HTTPConnection.send
    def new_send( self, data ):
        logging.debug(data)
        return old_send(self, data) #return is not necessary, but never hurts, in case the library is changed
    httplib.HTTPConnection.send= new_send


def json_dumps(obj):
    '''dump as utf-8 string instead of \uxxxx'''
    return json.dumps(obj,ensure_ascii=False,separators=(',', ':')).encode('utf-8')