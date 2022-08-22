"""
    A module for Abstract Metadata Fetcher
"""

from abc import ABCMeta, abstractmethod


class MetadataFetcher(metaclass=ABCMeta):
    """Abstract Feature Metadata Fetcher that fetch metadata from external data sources"""

    def __init__(self):
        self.session = None

    @abstractmethod
    def _get_or_create_session(self, conn_conf: object):
        """Protected Abstract method for getting or create session
        :return:
        """
        # todo - singleton session.
        return

    @abstractmethod
    def _get_dictionary_metadata(self):
        """Protected Abstract method for getting dictionary metadata

        :return:
        """
        return

    def fetch_metadata(self, conn_conf: object):
        """Template method that fetch metadata strongly protocolized with corresponding updater
        :return:
        """
        self._get_or_create_session(conn_conf)
        metadata = self._get_dictionary_metadata()
        return metadata
