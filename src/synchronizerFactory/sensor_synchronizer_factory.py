"""
    A module for Sensor and Position Metadata Synchronizer Factory class.
"""
from synchronizerFactory import SynchronizerFactory
from metadataFetcher import MetadataFetcher, SensorMetadataFetcher
from metadataUpserter import MetadataUpserter, SensorMetadataUpserter

class SensorSynchronizerFactory(SynchronizerFactory):
    """Concrete #1 Class from 'SynchronizerFactory'
    Sensor and Position Metadata Synchronizer Factory
     that yielding Sensor and Position Metadata Fetcher and Upserter.

    """

    def create_metadata_fetcher(self) -> MetadataFetcher:
        return SensorMetadataFetcher()

    def create_metadata_upserter(self) -> MetadataUpserter:
        return SensorMetadataUpserter()
