#!/usr/bin/env python
import webapp2
from handler import GeneralHandler
from login import LoginHandler
from logout import LogoutHandler
from signup import RegisterHandler, WelcomeHandler
from blogfunctions import NewPostHandler, PermalinkHandler, EditPostHandler, CommentHandler, EditCommentHandler, DeleteHandler
from likes import LikeHandler


# Main page displays only blog posts and menu
class MainPage(GeneralHandler):
    def get(self):
        posts = self.get_entries(100)
        user = self.user
        if user:
            username = user.name_by_user
            self.render('blog.html', posts = posts, user = user)
        else:
            self.render('blog.html', posts = posts)


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
    ('/comment', CommentHandler),
    ('/editcomment', EditCommentHandler),
    ('/delete', DeleteHandler)
    ], debug=True)
