"""This module provides general handling and helper functions, as well as Models
for users, posts and comments"""

import os

import jinja2

import webapp2
from handlers import helpers
from models.user import User
from models.post import Post


template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
print template_dir
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class GeneralHandler(webapp2.RequestHandler):
    """Handler that gets imported into more or less all other handlers that
    makes certain actions easier"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # get blog posts
    def get_entries(self, n=10):
        e = Post.query()
        e = e.order(-Post.created)
        entr = e.fetch(n)
        return entr

    # get comments
    def get_comments(self, n=10):
        c = Comment.query()
        c = c.order(-Comment.created)
        comments = c.fetch(n)
        return comments

    def render_single_comment(self, comment):
        """renders a single comment including all html, so that it can be inserted
        via ajax"""
        html = '''
                <div class="comment-edit-form col-xs-12">
                    <form method="post" class="edit-form">
                        <textarea name="edit-comment" class="comment-input col-xs-12">%s</textarea>
                        <a href="#" data-commentid="%s;%s" class="save-button">Save</a> |
                        <a href="#" class="cancel-button">Cancel</a>
                    </form>
                  <p class="error"><p>
                </div>
                <div class="single-comment single col-xs-12">
                    <p class="grey small border-top">%s said:</p>
                    <p class="comment-content">%s</p>
                    <a href="#" class="edit">Edit</a> |
                    <a href="#" data-ids="%d;%d" class="delete">Delete</a>
                </div>
                ''' % (comment.content, \
                       comment.key.id(), \
                       comment.key.parent().id(), \
                       comment.author_name, \
                       comment.content, \
                       comment.key.id(), \
                       comment.key.parent().id())
        return html

    def get_referrer(self):
        """get referrer or set referrer to index for use in cancel"""
        return self.request.referer or "/"

    def set_secure_cookie(self, name, val):
        """set the cookie with user id and hash"""
        cookie_val = helpers.make_secure_val(val.lower())
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path="/"'\
                                         % (name.lower(), cookie_val))

    def read_secure_cookie(self, name):
        """read the cookie and make sure the uid/hash pair is valid"""
        cookie_val = self.request.cookies.get(name)
        return cookie_val and helpers.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key.id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path="/"')

    def initialize(self, *a, **kw):
        """check if user is logged in and set global user if yes"""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
