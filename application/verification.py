import pylru
from random import choice
from string import ascii_uppercase

_cache = pylru.lrucache(1024)

def alloc_verification_code(data):
    v_code = (''.join(choice(ascii_uppercase) for i in range(16)))
    _cache[v_code] = data
    return v_code

def check_verification_code(v_code):
    if not(v_code in _cache):
        return None
    d = _cache[v_code]
    del _cache[v_code]
    return d

