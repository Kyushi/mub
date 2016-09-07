from handler import GeneralHandler
from signup import User

# Handler for login page, renders login form, checks input, sets cookie,
# redirects to welcome if user info is correct, otherwise displays error message
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
