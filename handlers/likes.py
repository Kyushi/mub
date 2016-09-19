"""This module contains only the 'like' class"""

import json

from models.post import Post
from handlers.generalhandler import GeneralHandler


# Handler for likes on posts
class LikeHandler(GeneralHandler):
    """Likes for posts are handled here"""
    def post(self):
        """Likes are updated dynamically via AJAX on the front end."""
        # this can only be reached if user is logged in, but just in case,
        #  we check for user:
        if self.user:
            # get post id from Ajax script
            post_id = int(self.request.get('postID'))
            # retrieve post entity from datastore
            post = Post.get_by_id(post_id)
            # retrieve user id from initialise method
            uid = self.user.key.id()
            # stop people from liking their own stuff
            if uid == post.author_key_id:
                error = "You can only rate others' comments"
                self.write(json.dumps(({'error': error})))
            elif uid in post.liked_by:
                post.likes -= 1
                post.liked_by.remove(uid)
                self.user.likes.remove(post.key.id())
                self.write(json.dumps(({'likes': post.likes, 'you-like': ''})))
                post.put()
                self.user.put()
            else:
                post.likes += 1
                post.liked_by.append(uid)
                self.user.likes.append(post.key.id())
                self.write(json.dumps(({'likes': post.likes, 'you-like': ' You like this'})))
                post.put()
                self.user.put()
        else:
            # just a fallback, it should never be displayed to a visitor, since
            # only logged in users get to see the link with the post method
            error = "Only logged in users can like posts"
            self.write(json.dumps(({'error': error})))
