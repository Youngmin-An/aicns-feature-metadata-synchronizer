"""
    A module for Abstract Metadata Upserter
"""

from abc import ABCMeta, abstractmethod


class MetadataUpserter(metaclass=ABCMeta):
    """Abstract Feature Metadata Upserter that upsert metadata to metadata store"""

    def __init__(self, client=None):
        self.client = client

    @abstractmethod
    def _get_or_create_client(self, conn_conf: object):
        """Protected Abstract method for getting or create metadata store client
        :return:
        """
        return

    @abstractmethod
    def _upsert_with_transaction(self, metadata):
        """Protected Abstract method for upserting metadata with application-level transaction

        :return:
        """
        return

    @abstractmethod
    def _close_client(self):
        """Protected Abstract method for closing metadata store client

        :return:
        """
        return

    def upsert_metadata(self, conn_conf: object, metadata):
        """Template method that upsert metadata strongly protocolized from corresponding metadata fetcher
        :return:
        """
        self._get_or_create_client(conn_conf)
        self._upsert_with_transaction(metadata)
        self._close_client()
        return
