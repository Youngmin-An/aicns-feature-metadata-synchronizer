"""
    This module for Abstract Synchronizer Factory class
"""

from abc import ABCMeta, abstractmethod


class SynchronizerFactory(metaclass=ABCMeta):
    """Abstract Synchronizer Factory that yields fetcher and saver."""

    @abstractmethod
    def create_metadata_fetcher(self):
        """This is a abstract factory method yielding metadata fetcher

        :return:
            Fetcher Object.
        """
        return

    @abstractmethod
    def create_metadata_saver(self):
        """This is a abstract factory method yielding metadata saver in data pipeline

        :return:
            Saver Object
        """
        return
