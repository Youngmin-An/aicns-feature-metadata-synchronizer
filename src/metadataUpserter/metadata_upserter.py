"""
    A module for Abstract Metadata Upserter
"""

from abc import ABCMeta, abstractmethod


class MetadataUpserter(metaclass=ABCMeta):
    """Abstract Feature Metadata Upserter that upsert metadata to metadata store"""

    def __init__(self, session=None):
        self.session = session

    @abstractmethod
    def _get_or_create_session(self, conn_conf: object):
        """Protected Abstract method for getting or create session
        :return:
        """
        return

    @abstractmethod
    def _upsert_with_transaction(self, metadata):
        """Protected Abstract method for upserting metadata with application-level transaction

        :return:
        """
        return

    def upsert_metadata(self, conn_conf: object, metadata):
        """Template method that upsert metadata strongly protocolized from corresponding metadata fetcher
        :return:
        """
        self._get_or_create_session(conn_conf)
        self._upsert_with_transaction(metadata)
        return