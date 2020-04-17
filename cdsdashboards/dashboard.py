import os
import json

from traitlets.config import LoggingConfigurable
from traitlets import Integer, Unicode, Bool
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from tornado.log import app_log
from tornado import web, gen


class DashboardRepr(LoggingConfigurable):
    """Object for an individual app/server for a user, such as files or repo and allowed visitors"""

    hub_api_token = Unicode(help="The API token for the Hub")
    hub_url = Unicode(help="The URL of the Hub")

    retries = Integer(
        4,
        config=True,
        help="""Number of attempts to make on Hub API requests.

        Adds resiliency to intermittent Hub failures,
        most commonly due to Hub, proxy, or ingress interruptions.
        """
    )
    retry_delay = Integer(
        4,
        config=True,
        help="""
        Time (seconds) to wait between retries for Hub API requests.

        Time is scaled exponentially by the retry attempt (i.e. 2, 4, 8, 16 seconds)
        """
    )

    async def get_user_data(self, username):
        resp = await self.api_request(
            'users/%s' % username,
            method='GET',
        )
        body = json.loads(resp.body.decode('utf-8'))
        return body

    async def get_app_server(self, username, server_name):
        user_data = await self.get_user_data(username)

        self.log.debug(user_data)

        if not server_name:
            return user_data.server
            
        if 'servers' in user_data and server_name in user_data['servers']:
            return user_data['servers'][server_name]
        
        return None

    async def api_request(self, url, *args, **kwargs):
        """Make an API request to JupyterHub"""
        headers = kwargs.setdefault('headers', {})
        headers.update({'Authorization': 'token %s' % self.hub_api_token})
        hub_api_url = os.getenv('JUPYTERHUB_API_URL', '') or self.hub_url + 'hub/api/'
        request_url = hub_api_url + url

        self.log.info("API call to {} with token {}".format(request_url, self.hub_api_token))

        req = HTTPRequest(request_url, *args, **kwargs, validate_cert=False)
        retry_delay = self.retry_delay
        for i in range(1, self.retries + 1):
            try:
                return await AsyncHTTPClient().fetch(req)
            except HTTPError as e:
                # swallow 409 errors on retry only (not first attempt)
                if i > 1 and e.code == 409 and e.response:
                    self.log.warning("Treating 409 conflict on retry as success")
                    return e.response
                # retry requests that fail with error codes greater than 500
                # because they are likely intermittent issues in the cluster
                # e.g. 502,504 due to ingress issues or Hub relocating,
                # 599 due to connection issues such as Hub restarting
                if e.code >= 500:
                    self.log.error("Error accessing Hub API (using %s): %s", request_url, e)
                    if i == self.retries:
                        # last api request failed, raise the exception
                        raise
                    await gen.sleep(retry_delay)
                    # exponential backoff for consecutive failures
                    retry_delay *= 2
                else:
                    raise
