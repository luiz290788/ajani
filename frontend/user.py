import httplib2

from google.appengine.api import memcache
from google.appengine.ext import ndb

from apiclient.discovery import build
from oauth2client.appengine import StorageByKeyName, CredentialsNDBModel

from auth_util import get_google_plus_user_id
from model import User

def getUser():
  user_id = get_google_plus_user_id()

  user = None

  if user_id is not None:
    user_key = ndb.Key(User, user_id)
    user = user_key.get()
    if user is None:
      user = User(gPlusId = user_id, id = user_id)
      user_key = user.put()

  return user

def getPersonalInfo(user):
  if type(user) is unicode:
    gPlusId = user
  elif user:
    gPlusId = user.gPlusId

  userInfo = memcache.get(gPlusId)

  if not userInfo:
    storage = StorageByKeyName(
      CredentialsNDBModel, gPlusId, 'credentials'
    )

    credentials = storage.get()

    if credentials:
      http = credentials.authorize(httplib2.Http())
      service = build('plus', 'v1', http=http)
      userInfo = service.people().get(userId='me').execute()
    else:
      if gPlusId:
        fakeName = gPlusId
      else:
        fakeName = user
      return {'displayName': fakeName, 
        'name': {'givenName': fakeName}, 
        'image': {'url': '/images/default-user.jpg'}}

      memcache.set(userInfo['id'], userInfo)

  return userInfo
