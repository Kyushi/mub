"""This module is for the Post model"""

from models.comment import Comment

from google.appengine.ext import ndb

class Post(ndb.Model):
    """Model for blog Post"""
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty()
    author = ndb.StringProperty(required=True)
    author_key_id = ndb.IntegerProperty()
    likes = ndb.IntegerProperty()
    liked_by = ndb.IntegerProperty(repeated=True)

    def render(self):
        """helper function to render blog text with line breaks"""
        self._render_text = self.content.replace('\n', '\n<br>')
        return self._render_text

    def get_comments(self):
        """helper function to display fetch all comments for their respective
        post from the datastore"""
        self.comments = Comment.query(ancestor=self.key).order(-Comment.created).fetch()
        return self.comments

    @classmethod
    def write_entity(cls, subject, content, author, author_key_id):
        """Class method to write a post entity to the datastore"""
        return cls(subject=subject,
                   content=content,
                   author=author,
                   author_key_id=author_key_id,
                   likes=0)
