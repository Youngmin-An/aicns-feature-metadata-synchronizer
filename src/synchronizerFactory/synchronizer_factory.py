"""
    This module for Abstract Synchronizer Factory class
"""

from abc import ABCMeta, abstractmethod


class SynchronizerFactory(metaclass=ABCMeta):
    """Abstract Synchronizer Factory that yields fetcher and upserter."""

    @abstractmethod
    def create_metadata_fetcher(self):
        """This is a abstract factory method yielding metadata fetcher

        :return:
            Fetcher Object.
        """
        return

    @abstractmethod
    def create_metadata_upserter(self):
        """This is a abstract factory method yielding metadata upserter in data pipeline

        :return:
            Upserter Object
        """
        return
