import requests
import logging
import time


from amocrm.url_builder import URLBuilder

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


class AmoCRMClient(object):

    def __init__(self, user, hash, subdomain, use_json=True):
        """
        Default constructor for the AMO CRM Client
        :param user: email for AMO CRM
        :param hash: hash for the given user, obtained from the UI profile_edit page
        :param subdomain: subdomain for company
        :param use_json: transform responses into JSON
        """
        logger.debug(
            "Configuring client with user: {user}, hash: {hash}, subdomain: {subdomain}, use_json: {use_json}".format(
                **{
                    "user": user,
                    "hash": hash,
                    "subdomain": subdomain,
                    "use_json": use_json
                }
            )
        )
        self._user = user
        self._hash = hash
        self._subdomain = subdomain
        self._use_json = use_json
        self._session = requests.Session()
        self.url_builder = URLBuilder(self._subdomain, use_json)

    def login(self):
        """
        Log into the AMO CRM, this is required before all requests
        """
        login_data = {
            "USER_LOGIN": self._user,
            "USER_HASH": self._hash
        }
        logger.debug("Trying to do login with data")
        logger.debug(login_data)
        login_response = self._session.post(
            self.url_builder.get_url_for(URLBuilder.LOGIN_ENDPOINT),
            json=login_data
        )
        logger.debug("Login status_code: {}".format(login_response.status_code))
        if login_response.ok:
            logger.debug(login_response.json() if self._use_json else login_response.content)

    def get_pipelines(self):
        """
        Return all the existing pipelines related to that user
        :return:
        """
        pipelines_response = self._session.get(
            self.url_builder.get_url_for(URLBuilder.GET_PIPELINES)
        )
        logger.debug("Get pipelines status_code: {}".format(pipelines_response.status_code))
        if pipelines_response.ok:
            return pipelines_response.json() if self._use_json else pipelines_response.content

    def get_single_pipeline(self, pipeline_id):
        pipelines_response = self._session.get(
            self.url_builder.get_url_for(URLBuilder.GET_PIPELINES, extra_params={"id": pipeline_id})
        )
        logger.debug("Get pipelines status_code: {}".format(pipelines_response.status_code))
        if pipelines_response.ok:
            return pipelines_response.json() if self._use_json else pipelines_response.content

    def add_pipeline(self, name, statuses, is_main=False, sort=0):
        """
        Add a new pipeline
        :param name: Name for the pipeline
        :param statuses: Dictionay with statuses configuration example: {
            "white_status":
                {
                    "color": "#ffffff",
                    "name": "White status",
                    "sort": 1
                }
            }
        :param is_main: Boolean that indicates if the pipeline is the main pipeline
        :param sort: Integer that indicates the order for the pipeline
        :return:
        """
        pipeline_data = {
            "request": {
                "pipelines": {
                    "add": [
                        {
                            "name": name,
                            "statuses": statuses,
                            "is_main": is_main,
                            "sort": sort,
                        }
                    ]
                }

            }

        }
        logger.debug("Pipeline creation data")
        logger.debug(pipeline_data)
        pipelines_response = self._session.post(
            self.url_builder.get_url_for(URLBuilder.SET_PIPELINES),
            json=pipeline_data
        )
        if pipelines_response.ok:
            return pipelines_response.json() if self._use_json else pipelines_response.content

    def update_pipeline(self, pipeline_id, name, statuses, is_main=False, sort=0):
        """
        Update a pipeline
        :param name: Name for the pipeline
        :param statuses: Dictionay with statuses configuration example: {
            "white_status":
                {
                    "color": "#ffffff",
                    "name": "White status",
                    "sort": 1
                }
            }
        :param is_main: Boolean that indicates if the pipeline is the main pipeline
        :param sort: Integer that indicates the order for the pipeline
        :return:
        """
        pipeline_data = {
            "request": {
                "pipelines": {
                    "update": {
                        pipeline_id: {
                            "name": name,
                            # "statuses": statuses,
                            "is_main": is_main,
                            "sort": sort,
                        }
                    }
                }
            }

        }
        logger.debug("Pipeline update data")
        logger.debug(pipeline_data)
        pipelines_response = self._session.post(
            self.url_builder.get_url_for(URLBuilder.SET_PIPELINES),
            json=pipeline_data
        )
        if pipelines_response.ok:
            return pipelines_response.json() if self._use_json else pipelines_response.content

    def delete_pipeline(self, pipeline_id):
        """
        Delete a pipeline
        :param pipeline_id: ID for the corresponding pipeline
        :return:
        """
        pipeline_data = {
            "request": {
                "id": pipeline_id
            }

        }
        logger.debug("Pipeline delete data")
        logger.debug(pipeline_data)
        pipelines_response = self._session.post(
            self.url_builder.get_url_for(URLBuilder.DELETE_PIPELINES),
            json=pipeline_data
        )
        if pipelines_response.ok:
            return pipelines_response.json() if self._use_json else pipelines_response.content

    def add_lead(self, name, pipeline_id, status_id, extra_args=None):
        """
        Add a lead
        :param name: Name of the lead
        :param pipeline_id: pipeline_id
        :param status_id: status_id
        :param extra_args: dictionary with extra args
        :return:
        """
        lead_data = {
            "name": name,
            "pipeline_id": pipeline_id,
            "status_id": status_id
        }

        if extra_args is not None:
            if isinstance(extra_args, dict):
                lead_data.update(extra_args)
            else:
                logger.error("extra_args of type {} is not supported".format(type(extra_args)))
                raise ValueError("extra_args of type {} is not supported".format(type(extra_args)))
        logger.debug("Lead adddata")
        logger.debug(lead_data)

        lead_wrapper = {
            "add": [
                lead_data
            ]
        }
        lead_response = self._session.post(
            self.url_builder.get_url_for(URLBuilder.SET_LEADS),
            json=lead_wrapper
        )
        if lead_response.ok:
            return lead_response.json() if self._use_json else lead_response.content

    def get_leads(self, offset=0):
        """
        Get 500 leads
        :param offset:
        :return:
        """
        lead_response = self._session.get(
            self.url_builder.get_url_for(URLBuilder.SET_LEADS),
        )
        if lead_response.ok:
            return lead_response.json() if self._use_json else lead_response.content

    def get_single_lead(self, id):
        """
                Get 500 leads
                :param offset:
                :return:
                """
        lead_response = self._session.get(
            self.url_builder.get_url_for(URLBuilder.SET_LEADS, {"id": id}),
        )
        if lead_response.ok:
            return lead_response.json() if self._use_json else lead_response.content

    def move_lead_to_next_status(self, lead_id, new_status_id):
        """
        Move a lead to a new column
        :param lead_id: Lead id
        :param new_status_id: New status id
        :return:
        """
        lead_data = {
            "update": [
                {
                    "id": lead_id,
                    "status_id": new_status_id,
                    "updated_at": int(time.time())
                }
            ]
        }
        logger.debug("Lead adddata")
        logger.debug(lead_data)
        lead_response = self._session.post(
            self.url_builder.get_url_for(URLBuilder.SET_LEADS),
            json=lead_data
        )
        if lead_response.ok:
            return lead_response.json() if self._use_json else lead_response.content
