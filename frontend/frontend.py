import webapp2
import httplib2
import jinja2
import socket

from google.appengine.api import memcache
from google.appengine.ext import ndb

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.appengine import StorageByKeyName, CredentialsNDBModel

from model import User

from config import CONFIG

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(CONFIG['templates_dir']))

flow = OAuth2WebServerFlow(
  client_id = CONFIG['credentials']['client_id'],
  client_secret = CONFIG['credentials']['client_secret'],
  scope = CONFIG['scope'],
  redirect_uri = 'https://' + socket.gethostname() + '/callback',
  approval_prompt = 'force')

class Homepage(webapp2.RequestHandler):

  def get(self):
    self.template_values = {
      'login_url': flow.step1_get_authorize_url()
    }

    template = jinja_environment.get_template('homepage.template')
    self.response.out.write(template.render(self.template_values))

class Oauth2Callback(webapp2.RequestHandler):

  def get(self):
    credentials = flow.step2_exchange(self.request.params)

    http = credentials.authorize(httplib2.Http())
    service = build('plus', 'v1', http=http)
    user = service.people().get(userId='me').execute()

    user_id = user['id']
    storage = StorageByKeyName(
      CredentialsNDBModel, user_id, 'credentials'
    )
    storage.put(credentials)

    memcache.set(user_id, user)

    user_key = ndb.Key(User, user_id)
    user = user_key.get()
    if user is None:
      user = User(gPlusId = user_id, id = user_id)
      user_key = user.put()

    self.redirect('/')

application = webapp2.WSGIApplication([
  ('/callback', Oauth2Callback),
  (r'/.*?', Homepage)
], debug=True)
