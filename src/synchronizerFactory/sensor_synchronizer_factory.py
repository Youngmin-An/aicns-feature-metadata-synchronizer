"""
    A module for Sensor and Position Metadata Synchronizer Factory class.
"""
from synchronizer_factory import SynchronizerFactory
from ..metadataFetcher import MetadataFetcher, SensorMetadataFetcher


class SensorSynchronizerFactory(SynchronizerFactory):
    """Concrete #1 Class from 'SynchronizerFactory'
    Sensor and Position Metadata Synchronizer Factory
     that yielding Sensor and Position Metadata Fetcher and Saver.

    """

    def create_metadata_fetcher(self) -> MetadataFetcher:
        return SensorMetadataFetcher()

    def create_metadata_saver(self):
        pass
