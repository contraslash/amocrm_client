from amocrm import conf


class URLBuilder(object):

    LOGIN_ENDPOINT = "login"

    ENDPOINTS = {
        LOGIN_ENDPOINT: conf.AMOCRM_LOGIN_URL,

    }

    def __init__(self, subdomain, use_json=True):
        self._subdomain = subdomain
        self._use_json = use_json

    def build_query_params(self, extra_params=None):
        params = dict()
        if self._use_json:
            params["type"] = "json"
        if extra_params is not None:
            if isinstance(extra_params, dict):
                params.update(extra_params)
            else:
                raise ValueError("Extra params type not supported, must be a dict-like instance")

        return "&".join(("{}={}".format(k, v) for k, v in extra_params.items()))

    def get_url_for(self, endpoint, extra_params=None):
        assert endpoint in self.ENDPOINTS
        return "{}{}?{}".format(
            conf.AMOCRM_BASE_URL.format(self._subdomain),
            self.ENDPOINTS[endpoint],
            self.build_query_params(extra_params)
        )