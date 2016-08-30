
import json
from handler import GeneralHandler, Entries, User

class LikeHandler(GeneralHandler):
    def post(self):
        if self.user:
            # get entry id from Ajax script
            entryID = int(self.request.get('entryID'))
            # retrieve entry entity from datastore
            entry = Entries.get_by_id(entryID)
            # retrieve user id from initialise function
            uid = self.user.key.id()
            # stop people from liking their own stuff
            if uid == entry.author_key:
                error = "You can only rate others' comments"
                self.write(json.dumps(({'error': error})))
            elif uid in entry.liked_by:
                entry.likes -= 1
                entry.liked_by.remove(uid)
                self.user.likes.remove(entry.key.id())
                self.write(json.dumps(({'likes': entry.likes, 'you-like': ''})))
                entry.put()
                self.user.put()
            else:
                entry.likes += 1
                entry.liked_by.append(uid)
                self.user.likes.append(entry.key.id())
                self.write(json.dumps(({'likes': entry.likes, 'you-like': 'You like this'})))
                entry.put()
                self.user.put()
        else:
            error = "You have to be logged in to post, comment or like"
            self.write(json.dumps(({'error': error})))
