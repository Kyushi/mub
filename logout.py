from handler import GeneralHandler

class LogoutHandler(GeneralHandler):
    def get(self):
        self.logout()
        self.redirect('/login')
