import boxsdk
import click as click
import requests
import logging
import webbrowser

import box_archive.helpers.constants as constants

from box_archive.helpers.Singleton import Singleton
from box_archive.helpers.boxauth import TokenHandler, BoxLoginError

logger = logging.getLogger(__name__)

@Singleton
class BoxAccess:

    def __init__(self):
        pass

    def login_prompt(self):
        oauth = boxsdk.OAuth2(
            client_id=constants.client_id,
            client_secret=constants.client_secret,
            store_tokens=self.save_tokens
        )
        auth_url, csrf_token = oauth.get_authorization_url("http://localhost:8080/")

        logger.info("Auth url: {0}, csrf_token: {1}", auth_url, csrf_token)
        try:
            auth_code = TokenHandler().get_access_token(auth_url)
        except BoxLoginError as e:
            click.secho("Authentication failed due to error: {0}".format(str(e)), fg='red', bold=True)
            exit(1)

        logger.info("AUTH_CODE: {0}", auth_code)
        oauth.authenticate(auth_code)
        # Create the SDK client
        client = boxsdk.LoggingClient(oauth)

        #Get logged in user
        user = client.user(user_id='me').get()
        print(user)
        pass

    def save_tokens(self, access_token, refresh_token):
        logger.debug('Access token: {0}, refresh token: {1}'.format(access_token, refresh_token))
        pass

    pass
