import os
import jinja2
import webapp2
import datetime
import json

from google.appengine.ext import ndb
from handler import GeneralHandler, Entries, Comment

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class CommentHandler(GeneralHandler):
    def post(self):
        if self.user:
            comment = self.request.get('comment')
            parent = Entries.get_by_id(int(self.request.get('parent')))
            entries = self.get_entries(100)
            comments = self.get_comments(100)
            uid = self.user.key.id()
            if not comment:
                self.render('comments.html', entries = entries, comments = comments, error = "Please type a comment" )
            else:
                c = Comment(content = comment,
                            author = uid,
                            parent = parent.key)
                c_key = c.put()
                comments = Comment.query(ancestor=entry.key).fetch()
                self.render('comments.html', entries = entries, comments = comments)
        else:
            self.redirect('/error', error = "Commenting is for registered users only")


# New post page for submitting an entry
class NewPostHandler(GeneralHandler):
    def get(self):
        user = self.user
        if not user:
            self.redirect('/login')
        else:
            username = self.user.name_by_user
            entries = self.get_entries(5)
            self.render('newpost.html',
                        entries = entries,
                        user = user)

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        author = self.user.name_by_user

        # check if title and entry are present, else show error message
        if subject and content:
            e = Entries(subject = subject,
                        content = content,
                        author = author,
                        author_key = self.user.key.id(),
                        likes = 0,
                        )
            e.put() # shove the thing into the datastore and
            entry_id = e.key.id() # get its id and
            self.redirect('/%d' % entry_id) # show a single blog entry

        # if there's no title or no entry or neither, display error message and
        else:
            error = "Subject + Content = Valid Submission"
            self.render('newpost.html',
                        subject=subject,
                        content=content,
                        error=error)

class EditPostHandler(GeneralHandler):
    def get(self, entry_id):
        entry = Entries.get_by_id(int(entry_id))
        has_error = False
        user = self.user
        if not user:
            self.redirect('/login')
        elif not entry:
            print "there's no entry"
            error = "This post does not exist"
            has_error = True
        elif not user.name_by_user == entry.author:
            error = "You cannot edit someone else's post"
            has_error = True
        if has_error:
            self.render('error.html', error = error)
        else:
            self.render('/editpost.html', entry = entry)


    def post(self, entry_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
        entry = Entries.get_by_id(int(entry_id))
        entry.subject = subject
        entry.content = content
        entry.last_modified = datetime.datetime.now()
        entry.put()
        self.redirect('/%d' % int(entry_id))


class PermalinkHandler(GeneralHandler):
    def get(self, entry_id):
        entry = Entries.get_by_id(int(entry_id))
        if not entry:
            self.error(404)
            return

        self.render('/blog.html', entries = [entry], user = self.user)
