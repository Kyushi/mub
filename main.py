#!/usr/bin/env python

__author__ = "Franziskus Nakajima"
__copyright__ = "Copyright 2016, Franziskus Nakajima"
__credits__ = ["Franziskus Nakajima", "Steve Huffmann", "Abishek Ghosh", \
               "Udacity Forums", "Udacity"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Franziskus Nakajima"
__email__ = "info@franziskusnakajima.net"
__status__ = "WIP"

import webapp2
from handlers.generalhandler import GeneralHandler
from handlers.login import LoginHandler, \
                           LogoutHandler
from handlers.signup import RegisterHandler, \
                            WelcomeHandler
from handlers.blogfunctions import NewPostHandler, \
                                   PermalinkHandler, \
                                   EditPostHandler, \
                                   CommentHandler, \
                                   EditCommentHandler, \
                                   DeleteHandler
from handlers.likes import LikeHandler


# Main page displays only blog posts and menu
class MainPage(GeneralHandler):
    """Render frontpage"""
    def get(self):
        posts = self.get_entries(100)
        user = self.user
        if user:
            self.render('blog.html', posts=posts, user=user)
        else:
            self.render('blog.html', posts=posts)


# route handlers
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPostHandler),
    (r'/(\d+)', PermalinkHandler),
    (r'/editpost/(\d+)', EditPostHandler),
    ('/signup', RegisterHandler),
    ('/welcome', WelcomeHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/like', LikeHandler),
    ('/comment', CommentHandler),
    ('/editcomment', EditCommentHandler),
    ('/delete', DeleteHandler)
    ], debug=True)
