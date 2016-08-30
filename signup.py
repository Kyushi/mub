import re
from handler import GeneralHandler, make_secure_val, check_secure_val, User

# helper functions for signup
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


# Handler for the whole shebang
class SignupHandler(GeneralHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        # get user input and initialise error messages
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify = self.request.get("verify")
        self.email = self.request.get("email", "")
        self.error1 = self.error2 = self.error3 = self.error4 = ""

        # validate user input
        valid_username = validate_user(self.username.lower())
        valid_password = validate_pw(self.password)
        valid_verify = verify_password(self.password, self.verify)
        valid_email = validate_email(self.email)

        # set error messages if validation fails
        if not valid_username:
            self.error1 = "This is not a valid username"
        if not valid_password:
            self.error2 = "This is not a valid password"
        elif not valid_verify:
            self.error3 = "The passwords you entered don't match"
        if not valid_email:
            self.error4 = "This is not a valid e-mail address"


        # select what to show next
        if valid_username and valid_password and valid_verify and valid_email:
            self.done()
        else:
            self.render("signup.html", username = self.username,
                                       password = self.password,
                                       verify = self.verify,
                                       email = self.email,
                                       error1 = self.error1,
                                       error2 = self.error2,
                                       error3 = self.error3,
                                       error4 = self.error4)
    def done(self, *a, **kw):
        raise NotImplementedError

class RegisterHandler(SignupHandler):
    def done(self):
        u = User.by_name(self.username.lower())
        if u:
            self.error1 = "This username already exists"
            self.render("signup.html", error1 = self.error1)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            self.redirect('/welcome')

class WelcomeHandler(GeneralHandler):
    def get(self):
        user = self.user
        if user:
            self.render('welcome.html', user = user)
        else:
            self.redirect("/signup")
