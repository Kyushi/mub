"""This module handles all writing, editing and deleting of posts and
comments"""
import datetime
import json

from google.appengine.ext import ndb
from models.post import Post
from models.comment import Comment
from handlers.generalhandler import GeneralHandler


class NewPostHandler(GeneralHandler):
    """This class handles the new post page."""
    def get(self):
        """Method for rendering new post page. Only logged in users will see the
        page, everybody else gets redirected to the login page"""
        if not self.user:
            self.redirect('/login?er=1')
        else:
            posts = self.get_entries(100)
            referrer = self.get_referrer() # referrer that allows to return to
            self.render('newpost.html',    #  the previous page on cancel
                        posts=posts,
                        user=self.user,
                        referrer=referrer)

    def post(self):
        """Method to post a new blog post. Both subject and content are
        required, omitting either results in an error"""
        if not self.user:
            self.redirect('/login?er=1')
        else:
            subject = self.request.get('subject')
            content = self.request.get('content')
            author = self.user.name_by_user

            # check if title and post are present, else show error message
            if subject and content:
                post = Post.write_entity(subject,content,author,self.user.key.id())
                post.put() # shove the thing into the datastore and
                post_id = post.key.id() # get its id and
                self.redirect('/%d' % post_id) # show a single blog post

            # if there's no title or no post or neither, display error message
            else:
                error = "Subject + Content = Valid Submission"
                self.render('newpost.html',
                            subject=subject,
                            content=content,
                            error=error)

class EditPostHandler(GeneralHandler):
    """Class that handles the page to edit blog posts. Cancelling the editing
    of a post is handled via jQuery on the front end"""
    def get(self, entry_id):
        if not self.user:
            self.redirect('/login')
        else:
            post = Post.get_by_id(int(entry_id))
            has_error = False
            user = self.user
            referrer = self.get_referrer()
            if not post:
                error = "This post does not exist"
                has_error = True
            elif not user.name_by_user == post.author:
                error = "You cannot edit someone else's post"
                has_error = True
            if has_error:
                self.render('error.html', error=error)
            else:
                self.render('/editpost.html', user=user, post=post, referrer=referrer)


    def post(self, entry_id):
        if not self.user:
            self.redirect('/login?er=1')
        else:
            post = Post.get_by_id(int(entry_id))
            if post.author_key_id == self.user.key.id():
                post.subject = self.request.get('subject')
                post.content = self.request.get('content')
                post.last_modified = datetime.datetime.now()
                post.put()
                self.redirect('/%d' % int(entry_id))
            else:
                self.render('error.html',
                            error = "You are not authorised to edit this post.")


class PermalinkHandler(GeneralHandler):
    """Handler that allows for posts to have a permalink (post ID). If post
    doesn't exist, error message is displayed"""
    def get(self, entry_id):
        post = Post.get_by_id(int(entry_id))
        if not post:
            self.render('error.html', error="This post doesn't exist")
            return

        self.render('/blog.html', posts=[post], user=self.user)

class DeleteHandler(GeneralHandler):
    """DeleteHandler handles deletion of posts and comments"""
    def post(self):
        if not self.user:
            self.redirect('/login?er=1')
        else:
            #ids can be either comment and parent id or only post id
            ids = self.request.get('ids')
            if ';' in ids:
                data = ids.split(';')
                parentid = int(data[1])
                entityid = int(data[0])
                self.delete_comment(parentid, entityid)
                self.write(json.dumps(({})))
            else:
                self.delete_post(int(ids))
                self.write(json.dumps(({})))

    def delete_comment(self, parentid, entityid):
        """function to delete comment from datastore"""
        parent_key = Post.get_by_id(parentid).key
        comment = Comment.get_by_id(entityid, parent_key)
        comment_key = comment.key
        if self.user.key.id() == comment.author_key_id:
            comment_key.delete()
        return

    def delete_post(self, entityid):
        """function to delete post and all children from datastore. Children
        will not be displayed again, so deleting is best"""
        post = Post.get_by_id(entityid)
        if self.user.key.id() == post.author_key_id:
            ndb.delete_multi(ndb.Query(ancestor=post.key).iter(keys_only=True))
        return


# Everything for comments below except delete, which is above

class CommentHandler(GeneralHandler):
    """Handler for posting comments"""
    def post(self):
        """Posting a comment is only possible for users that are logged in.
        AJAX is used to update the comments on the front end dynamically."""
        if not self.user:
            self.redirect('/login?er=1')
        else:
            comment = self.request.get('comment')
            parent = Post.get_by_id(int(self.request.get('parent')))
            author_key_id = self.user.key.id()
            author_name = self.user.name_by_user
            if not comment:
                return # do nothing if user submitted empty comment
            else:
                c = Comment.write_entity(comment,
                                         author_key_id,
                                         author_name,
                                         parent.key)
                c.put()
                comment = self.render_single_comment(c)
                # return JSON to Ajax
                self.write(json.dumps(({'comment': comment})))


class EditCommentHandler(GeneralHandler):
    """Handler to edit comment in place"""
    def post(self):
        """Comments require the comment id as well as the parent key. Both are
        passed to the post method in a string, separated by semicolon"""
        if not self.user:
            self.redirect('/login?er=1')
        else:
            data = self.request.get('commentid').split(';')
            commentid = int(data[0])
            parentid = int(data[1])
            newcomment = self.request.get('newcomment')
            parent_key = Post.get_by_id(parentid).key
            comment = Comment.get_by_id(commentid, parent_key)
            if comment:
                if comment.author_key_id == self.user.key.id():
                    comment.content = newcomment
                    comment.put()
                    self.write(json.dumps(({'comment': \
                    self.render_commenttext(comment.content)})))
                else:
                    self.render('error.html', \
                                error = "You can't edit this comment")
            else:
                self.write(json.dumps(({'comment': "There was no comment"})))

    def render_commenttext(self, comment):
        """Helper function to render line breaks in comments"""
        comment = comment.replace('\n', '<br>')
        return comment
