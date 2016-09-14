"""This module provides global helper functions"""

import hmac
import random
import string
import hashlib

from google.appengine.ext import ndb
from handlers.secret import SECRET


def users_key(group='default'):
    """make users key (for possible later use to have user groups, such as
    admin, mod etc.)"""
    return ndb.Key('users', group)

# functions for hashing and checking hashed user login info
def make_salt():
    salt = ''.join(random.choice(string.letters) for x in xrange(7))
    return salt

def make_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s|%s" % (salt, h)

def valid_hash(name, pw, h):
    salt = h.split('|')[0]
    return h == make_hash(name, pw, salt)


# make uid|hash pair for cookie
def make_secure_val(val):
    return "%s|%s" %(val, hmac.new(SECRET, val).hexdigest())

# check uid/hash pair for validity
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
