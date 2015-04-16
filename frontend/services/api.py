import endpoints
from config import CONFIG

duels = endpoints.api(name='duels', version='v1',
  allowed_client_ids = [CONFIG['credentials']['client_id']])
