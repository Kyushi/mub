"""this module contains the model for Comments"""

from google.appengine.ext import ndb

class Comment(ndb.Model):
    """Model for comments"""
    content = ndb.StringProperty(required=True)
    author_id = ndb.IntegerProperty(required=True)
    author_name = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty()
    likes = ndb.IntegerProperty()
    liked_by = ndb.IntegerProperty(repeated=True)


    @classmethod
    def write_entity(cls,content,author_id,author_name,parent_key):
        return cls(content=content,
                   author_id=author_id,
                   author_name=author_name,
                   parent=parent_key)
