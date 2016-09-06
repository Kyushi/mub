import webapp2
import jinja2
import os
import hmac
import random
import string
import hashlib


from google.appengine.ext import ndb

secret = 'BWMJs?Tzp2WLGT*PNEv@7Fq5W9GtW#?7'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


# Model for blog Post
class Post(ndb.Model):
    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty()
    author = ndb.StringProperty(required = True)
    author_key = ndb.IntegerProperty()
    likes = ndb.IntegerProperty()
    liked_by = ndb.IntegerProperty(repeated = True)

    def render(self):
        self._render_text = self.content.replace('\n', '\n<br>')
        return self._render_text

    def comments(self):
        self.comments = Comment.query(ancestor=self.key).order(-Comment.created).fetch()
        return self.comments

# Model for comments:
class Comment(ndb.Model):
    content = ndb.StringProperty(required=True)
    author_id = ndb.IntegerProperty(required = True)
    author_name = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty()
    likes = ndb.IntegerProperty()
    liked_by = ndb.IntegerProperty(repeated = True)

# Model for users
class User(ndb.Model):
    username = ndb.StringProperty(required = True)
    name_by_user = ndb.StringProperty(required = True)
    pw_hash = ndb.StringProperty(required = True)
    email = ndb.StringProperty()
    register_date = ndb.DateTimeProperty(auto_now_add = True)
    likes = ndb.IntegerProperty(repeated = True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        return cls.query(cls.username == name).get()

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_hash(name.lower(), pw)
        return cls(parent = users_key(),
                   username = name.lower(),
                   name_by_user = name,
                   pw_hash = pw_hash,
                   email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name.lower())
        if u and valid_hash(name.lower(), pw, u.pw_hash):
            return u

# functions for hashing and checking hashed user login info
def make_salt():
    salt = ''.join(random.choice(string.letters) for x in xrange(7))
    return salt

def make_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s|%s" % (salt, h)

def valid_hash(name, pw, h):
    salt = h.split('|')[0]
    return h == make_hash(name, pw, salt)


# make uid|hash pair for cookie
def make_secure_val(val):
    return "%s|%s" %(val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

# make users key
def users_key(group = 'default'):
    return ndb.Key('users', group)


class GeneralHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get_entries(self, n=10):
        e = Post.query()
        e = e.order(-Post.created)
        entr = e.fetch(n)
        return entr

    def get_comments(self, n=10):
        c = Comment.query()
        c = c.order(-Comment.created)
        comments = c.fetch()
        return comments

    # TODO: render with edit and delete links
    def render_single_comment(self, comment):
        html = '''
                <div class="single-comment">
                    <p class="grey small">%s said:</p>
                    <p>%s</p>
        ''' % (comment.author_name, comment.content)
        if comment.author_name != "System":
            html += '''
                        <a href="#" class="edit">Edit</a> |
                        <a href="#" data-ids="%d;%d" class="delete">Delete</a>
                    </div>
                    ''' % (comment.key.id(), comment.key.parent().id())
        else:
            html += "\n</div>"
        return html

    def get_referrer(self):
        return self.request.referer or "/"

    def render_blog(self, page, **kw):
        e = Post.query()
        e = e.order(-Post.created)
        posts = e.fetch(10)
        for post in posts:
            print("Entry: %s" % str(post))
        self.render(page, posts = posts, **kw)

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val.lower())
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path="/"' % (name.lower(), cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key.id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path="/"')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
