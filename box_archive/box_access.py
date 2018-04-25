import boxsdk

from box_archive.helpers.Singleton import Singleton


@Singleton
class BoxAccess:

    def __init__(self):
        self.access_token = None
        pass

    @staticmethod
    def loginPrompt():
        pass

    pass
