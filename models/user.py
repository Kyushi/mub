"""This module contains the model for Users"""

from google.appengine.ext import ndb
from handlers import helpers


class User(ndb.Model):
    """Model for users"""
    username = ndb.StringProperty(required=True)
    name_by_user = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    register_date = ndb.DateTimeProperty(auto_now_add=True)
    likes = ndb.IntegerProperty(repeated=True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=helpers.users_key())

    @classmethod
    def by_name(cls, name):
        return cls.query(cls.username == name).get()

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = helpers.make_hash(name.lower(), pw)
        return cls(parent=helpers.users_key(),
                   username=name.lower(),
                   name_by_user=name,
                   pw_hash=pw_hash,
                   email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name.lower())
        if u and helpers.valid_hash(name.lower(), pw, u.pw_hash):
            return u
