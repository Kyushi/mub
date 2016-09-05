import os
import jinja2
import webapp2
import datetime
import json

from google.appengine.ext import ndb
from handler import GeneralHandler, Post, Comment

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)





# New post page for submitting an post
class NewPostHandler(GeneralHandler):
    def get(self):
        user = self.user
        if not user:
            self.redirect('/login')
        else:
            username = self.user.name_by_user
            posts = self.get_entries(5)
            referrer = self.get_referrer()
            print("Referrer on newpost: %s" % referrer)
            self.render('newpost.html',
                        posts = posts,
                        user = user,
                        referrer = referrer)

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        author = self.user.name_by_user

        # check if title and post are present, else show error message
        if subject and content:
            e = Post(subject = subject,
                     content = content,
                     author = author,
                     author_key = self.user.key.id(),
                     likes = 0
                     )
            e.put() # shove the thing into the datastore and
            entry_id = e.key.id() # get its id and
            self.redirect('/%d' % entry_id) # show a single blog post

        # if there's no title or no post or neither, display error message and
        else:
            error = "Subject + Content = Valid Submission"
            self.render('newpost.html',
                        subject=subject,
                        content=content,
                        error=error)

class EditPostHandler(GeneralHandler):
    def get(self, entry_id):
        post = Post.get_by_id(int(entry_id))
        has_error = False
        user = self.user
        referrer = self.get_referrer()
        if not post:
            print "there's no post"
            error = "This post does not exist"
            has_error = True
        if has_error:
            self.render('error.html', error = error)
        if not user:
            self.redirect('/login')
        elif not user.name_by_user == post.author:
            error = "You cannot edit someone else's post"
            has_error = True
        else:
            self.render('/editpost.html', user = user, post = post, referrer = referrer)


    def post(self, entry_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
        post = Post.get_by_id(int(entry_id))
        post.subject = subject
        post.content = content
        post.last_modified = datetime.datetime.now()
        post.put()
        self.redirect('/%d' % int(entry_id))

class PermalinkHandler(GeneralHandler):
    def get(self, entry_id):
        post = Post.get_by_id(int(entry_id))
        if not post:
            self.error(404)
            return

        self.render('/blog.html', posts = [post], user = self.user)

# TODO: Implement the following:
# DeleteHandler handles deletion of Posts and comments by replacing the content
# with a default notice and the author to a default setting. Everything else
# gets initialised
class DeleteHandler(GeneralHandler):
    def post(self):
        ids = self.request.get('ids')
        print("IDs: %s" % ids)
        if ';' in ids:
            print("It's a comment")
            data = ids.split(';')
            parentid = int(data[1])
            entityid = int(data[0])
            comment = self.delete_comment(parentid, entityid)
            self.write(json.dumps(({'comment': self.render_single_comment(comment)})))
        else:
            print("It's a post")
            self.delete_post(int(ids))
            self.redirect(self.request.referer)

    def delete_comment(self, parentid, entityid):
        parent_key = Post.get_by_id(parentid).key
        print "pk", parent_key
        comment = Comment.get_by_id(entityid, parent_key)
        comment.content = "This comment was deleted by the user"
        comment.author_name = "System"
        comment.author_id = 0
        comment.created = datetime.datetime.now()
        comment.last_modified = None
        comment.likes = 0
        comment.liked_by = []
        comment.put()
        return comment

    def delete_post(self, entityid):
        post = Post.get_by_id(entityid)
        post.subject = "Deleted Post"
        post.content = "This post was deleted by the user"
        post.author = "System"
        post.author_key = 0
        post.created = datetime.datetime.now()
        post.last_modified = None
        post.likes = 0
        post.liked_by = []
        post.put()
        return post


# Everything for comments below

class CommentHandler(GeneralHandler):
    def post(self):
        if self.user:
            comment = self.request.get('comment')
            parent = Post.get_by_id(int(self.request.get('parent')))
            posts = self.get_entries(100)
            comments = self.get_comments(100)
            author_id = self.user.key.id()
            author_name = self.user.name_by_user
            if not comment:
                return
            else:
                c = Comment(content = comment,
                            author_id = author_id,
                            author_name = author_name,
                            parent = parent.key)
                c.put()
                comment = self.render_single_comment(c)
                self.write(json.dumps(({'comment': comment})))
        else:
            self.redirect('/error', error = "Commenting is for registered users only")

# edit comment in place
class EditCommentHandler(GeneralHandler):
    def post(self):
        data = self.request.get('commentid').split(';')
        commentid = int(data[0])
        parentid = int(data[1])
        newcomment = self.request.get('newcomment')
        print("Comment text: ", newcomment)
        parent_key = Post.get_by_id(parentid).key
        comment = Comment.get_by_id(commentid, parent_key)
        if comment:
            comment.content = newcomment
            comment.put()
            self.write(json.dumps(({'comment': self.render_commenttext(comment.content)})))
        else:
            self.write(json.dumps(({'comment': "There was no comment"})))

    def render_commenttext(self, comment):
        comment = comment.replace('\n', '<br>')
        return comment
