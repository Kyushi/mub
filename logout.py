from handler import GeneralHandler

# Logout handler, removes user info from cookie, redirects to login page
class LogoutHandler(GeneralHandler):
    def get(self):
        self.logout()
        self.redirect('/login')
