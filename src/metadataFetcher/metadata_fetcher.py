"""
    A module for Abstract Metadata Fetcher
"""

from abc import ABCMeta, abstractmethod


class MetadataFetcher(metaclass=ABCMeta):
    """Abstract Feature Metadata Fetcher that fetch metadata from external data sources"""

    @abstractmethod
    def __get_or_create_session(self, conn_conf: object):
        """Protected Abstract method for getting or create session
        :return:
        """
        # todo - singleton session.
        return

    @abstractmethod
    def __get_jsonified_metadata(self):
        """Protected Abstract method for getting jsonified metadata

        :return:
        """
        return

    def fetch_metadata(self, conn_conf: object):
        """Template method that fetch metadata strongly protocolized with corresponding updater
        :return:
        """
        session = self.__get_or_create_session(conn_conf)
        json_metadata = self.__get_jsonified_metadata(session)
        return json_metadata
