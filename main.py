#!/usr/bin/env python
import webapp2
from handler import GeneralHandler
from login import LoginHandler
from logout import LogoutHandler
from signup import RegisterHandler, WelcomeHandler
from blogfunctions import NewPostHandler, PermalinkHandler, EditPostHandler, CommentHandler
from likes import LikeHandler


# Main page displays only blog entries and menu
class MainPage(GeneralHandler):
    def get(self):
        entries = self.get_entries(100)
        comments = self.get_comments(100)
        user = self.user
        if user:
            username = user.name_by_user
            self.render('comments.html', entries = entries, comments = comments, user = user)
        else:
            self.render('comments.html', entries = entries, comments = comments)


# make things work
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPostHandler),
    ('/(\d+)', PermalinkHandler),
    ('/editpost/(\d+)', EditPostHandler),
    ('/signup', RegisterHandler),
    ('/welcome', WelcomeHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/like', LikeHandler),
    ('/comment', CommentHandler)
    ], debug=True)
