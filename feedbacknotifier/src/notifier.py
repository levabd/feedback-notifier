# coding=utf-8

from lib import logger


class Notifier(object):

    def __init__(self, base_path, googleplay_key_file, applestore_app_id):
        """
        :param base_path:
        :param googleplay_key_file:
        :param applestore_app_id:
        """
