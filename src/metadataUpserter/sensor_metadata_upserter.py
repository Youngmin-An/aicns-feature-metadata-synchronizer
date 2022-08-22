"""
    A module for sensor and position metadata upserter class (Concrete 1)
"""

from metadataUpserter import MetadataUpserter
from pymongo import MongoClient


import logging

logger = logging.getLogger(__name__)


class SensorMetadataUpserter(MetadataUpserter):
    """Concrete #1 Class from 'MetadataUpserter'
    Sensor and Position Metadata Upserter
     that connect to metadata store and upsert feature metadata"""

    def _get_or_create_client(self, conn_conf: object):
        """
        :return:
        """
        logger.debug("Entered '__get_or_create_client'")
        if self.client is None:
            # No exception handling so as to fail process
            logger.debug("Not yet has client")
            if "url" in conn_conf.keys():
                url = conn_conf["url"]
            else:
                url = f"mongodb://{conn_conf['addr']}:{conn_conf['port']}/"
            client = MongoClient(url)
            self.client = client
            logger.info(f"Client object created: {self.client}")
        else:
            logger.debug("Already has client")
        return self.client
