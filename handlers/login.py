"""This module handles the login page"""

from handlers.generalhandler import GeneralHandler
from models.user import User

# Handler for login page, renders login form, checks input, sets cookie,
# redirects to welcome if user info is correct, otherwise displays error message
class LoginHandler(GeneralHandler):
    """This class handles the login page"""
    def get(self):
        error = self.request.get('er')
        if error:
            error_message = """You can only write, edit, delete or like posts or
                            comments after logging in. If you haven't signed up yet,
                            please do so."""
        else:
            error_message = None
        self.render('login.html', error = error_message)

    def post(self):
        name_by_user = self.request.get("username")
        username = name_by_user.lower()
        password = self.request.get("password")

        # check if user input is valid
        u = User.login(username, password)
        if not u:
            error = "Your login information was incorrect"
            self.render('login.html', error=error, username=name_by_user)
        else:
            self.login(u)
            self.redirect('/welcome')


# Logout handler, removes user info from cookie, redirects to login page
class LogoutHandler(GeneralHandler):
    """This class handles the logout"""
    def get(self):
        self.logout()
        self.redirect('/login')
