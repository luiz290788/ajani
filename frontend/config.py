import os

CONFIG = {
  'templates_dir': os.path.dirname(__file__) + '/templates',
  'credentials': {
    'client_id': '246410276514-19obm550uk64bf6io6itmj9n02on1aq7.apps.googleusercontent.com',
    'client_secret': 'qjj8vqkA6Mp9iF1IrbVd_All'
  },
  'scope': ['https://www.googleapis.com/auth/plus.login',
            'https://www.googleapis.com/auth/plus.me',
            'https://www.googleapis.com/auth/plus.profiles.read',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile']
}
