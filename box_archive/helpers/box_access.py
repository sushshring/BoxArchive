import boxsdk
import click as click
import logging
import keyring

import box_archive.helpers.constants as constants

from box_archive.helpers.Singleton import Singleton
from box_archive.helpers.boxauth import TokenHandler, BoxLoginError
from boxsdk.exception import BoxException

logger = logging.getLogger('box_archive')


@Singleton
class BoxAccess:

    def __str__(self) -> str:
        try:
            return "Logged in: {0} | oauth: {1}".format(self.logged_in, self.oauth)
        except AttributeError:
            return "Logged in: {0}".format(self.logged_in)

    def __init__(self):
        """

        """
        self.logged_in = False
        access_token = keyring.get_password("Box Access", constants.BOX_ACCESS_TOKEN_KEY)
        refresh_token = keyring.get_password("Box Access", constants.BOX_ACCESS_REFRESH_KEY)
        if access_token and refresh_token:
            self.oauth = boxsdk.OAuth2(
                client_id=constants.client_id,
                client_secret=constants.client_secret,
                access_token=access_token,
                refresh_token=refresh_token
            )
            self.client = boxsdk.Client(self.oauth)
            try:
                if self.client.user(user_id='me').get():
                    self.logged_in = True
                    pass
                pass
            except BoxException as e:
                self.login_prompt()
                self.logged_in = True
        pass

    def login_prompt(self):
        """
        Launches a login prompt for Box Authentication
        :return:
        """
        self.oauth = boxsdk.OAuth2(
            client_id=constants.client_id,
            client_secret=constants.client_secret,
            store_tokens=self.save_tokens
        )
        auth_url, csrf_token = self.oauth.get_authorization_url("http://localhost:8080/")

        logger.info("Auth url: {0}, csrf_token: {1}", auth_url, csrf_token)
        try:
            auth_code = TokenHandler().get_access_token(auth_url)
        except BoxLoginError as e:
            click.secho("Authentication failed due to error: {0}".format(str(e)), fg='red', bold=True)
            exit(1)

        logger.info("AUTH_CODE: {0}", auth_code)
        self.oauth.authenticate(auth_code)
        # Create the SDK client
        print(logger.getEffectiveLevel())
        if logger.getEffectiveLevel() == logging.DEBUG:
            self.client = boxsdk.LoggingClient(self.oauth)
        else:
            self.client = boxsdk.Client(self.oauth)
        pass

    def get_user(self):
        return self.client.user(user_id='me').get()

    @staticmethod
    def save_tokens(access_token, refresh_token):
        """
        Saves the access_token and refresh_token to the system keyring
        :param access_token:
        :param refresh_token:
        :return:
        """
        logger.debug('Access token: {0}, refresh token: {1}'.format(access_token, refresh_token))
        keyring.set_password("Box Access", constants.BOX_ACCESS_TOKEN_KEY, access_token)
        keyring.set_password("Box Access", constants.BOX_ACCESS_REFRESH_KEY, refresh_token)
        pass


pass
