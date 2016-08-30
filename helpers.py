import jinja2
import hmac
SECRET = "thisisnotevenhere"

# global helper functions
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if make_secure_val(val) == h:
        return val
