
import json
from handler import GeneralHandler, Post, User

class LikeHandler(GeneralHandler):
    def post(self):
        if self.user:
            # get post id from Ajax script
            postID = int(self.request.get('postID'))
            # retrieve post entity from datastore
            post = Post.get_by_id(postID)
            # retrieve user id from initialise function
            uid = self.user.key.id()
            # stop people from liking their own stuff
            if uid == post.author_key:
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
                self.write(json.dumps(({'likes': post.likes, 'you-like': 'You like this'})))
                post.put()
                self.user.put()
        else:
            error = "You have to be logged in to post, comment or like"
            self.write(json.dumps(({'error': error})))
            self.redirect('/login')
            print "Redirected"
