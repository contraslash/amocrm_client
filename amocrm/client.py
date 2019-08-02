import requests

from amocrm.utils import URLBuilder



class AmoCRMClient(object):

    def __init__(self, user, hash, subdomain, use_json=True):
        self._user = user,
        self._hash = hash
        self._subdomain = subdomain
        self._session = requests.Session()
        self.url_builder = URLBuilder(self._subdomain, use_json)

    def login(self):
        self._session.post(
            self.url_builder.get_url_for(URLBuilder.LOGIN_ENDPOINT)
        )

