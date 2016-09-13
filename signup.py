"""This module handles the user signup"""

import re
from handler import GeneralHandler, User

# helper functions to verify user input
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validate_user(username):
    return USER_RE.match(username)

PW_RE = re.compile(r"^.{3,20}$")
def validate_pw(password):
    return PW_RE.match(password)

def verify_password(password, verify):
    return verify == password

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def validate_email(email):
    return EMAIL_RE.match(email) or True


class SignupHandler(GeneralHandler):
    """Handler for the signup page"""
    def get(self):
        self.render("signup.html")

    def post(self):
        """Upon posting the signup form we validate user input"""
        # get user input and initialise error messages
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify = self.request.get("verify")
        self.email = self.request.get("email")
        self.error1 = self.error2 = self.error3 = self.error4 = ""

        # validate user input
        valid_username = validate_user(self.username.lower())
        valid_password = validate_pw(self.password)
        valid_verify = verify_password(self.password, self.verify)
        valid_email = validate_email(self.email)
        print('Valid email: ', valid_email)

        # set error messages if validation fails
        if not valid_username:
            self.error1 = "This is not a valid username"
        if not valid_password:
            self.error2 = "This is not a valid password"
        elif not valid_verify:
            self.error3 = "The passwords you entered don't match"
        if not valid_email:
            self.error4 = "This is not a valid e-mail address"


        # if all input is valid, coninue with done in RegisterHandler
        if valid_username and valid_password and valid_verify and valid_email:
            self.done()
        # if there is an error, render signup form with user input and error
        # messages
        else:
            self.render("signup.html",
                        username=self.username,
                        password=self.password,
                        verify=self.verify,
                        email=self.email,
                        error1=self.error1,
                        error2=self.error2,
                        error3=self.error3,
                        error4=self.error4)

    def done(self, *a, **kw):
        """This is just a placeholder which does not get called"""
        raise NotImplementedError

# this handles the actual registration
class RegisterHandler(SignupHandler):
    """This class handles the actual registration after validation"""
    def done(self):
        """We're using the done method here since we inherit from the
        SignupHandler"""
        # check if username is already registered
        u = User.by_name(self.username.lower()) # case doesn't matter
        if u:
            self.error1 = "This username already exists"
            self.render("signup.html", error1=self.error1)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            self.redirect('/welcome')

class WelcomeHandler(GeneralHandler):
    """Render welcome page if user signed up successfully,
    otherwise redirect to signup"""
    def get(self):
        user = self.user
        if user:
            self.render('welcome.html', user=user)
        else:
            self.redirect("/signup")
