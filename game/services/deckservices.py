import os, requests
from google.appengine.api import modules

MODULE_HOST = modules.get_hostname(module='deck')

def _is_dev():
  return os.environ['SERVER_SOFTWARE'].startswith('Development')

def init_base_url():
  if _is_dev():
    base_url_pattern = 'http://%s/'
  else:
    base_url_pattern = 'https://%s/'
  return base_url_pattern % MODULE_HOST

BASE_URL = init_base_url()

def get(deck_id):
  url = BASE_URL + 'api/deck/' + str(deck_id)
  result = requests.get(url)
  return result.json()
  