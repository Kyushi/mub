from handler import GeneralHandler, make_hash, valid_hash
from signup import User
from google.appengine.ext import ndb

# make hash with username entered by user and salt from db
def check_hash(pw_hash, pw):
    salt = pw_hash.split('|')[0]
    return make_hash(pw, salt) == pw_hash

class LoginHandler(GeneralHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        name_by_user = self.request.get("username")
        username = name_by_user.lower()
        password = self.request.get("password")

        u = User.login(username, password)
        if not u:
            error = "Your login information was incorrect"
            self.render('login.html', error = error, username = name_by_user)
        else:
            self.login(u)
            self.redirect('/welcome')
