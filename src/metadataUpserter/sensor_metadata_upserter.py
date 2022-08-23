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

    def _upsert_with_transaction(self, metadata):
        """Upsert feature metadata within transaction

        :param metadata:
        :return:
        """
        logger.debug("Entered _upsert_with_transaction")
        with self.client.start_session() as session:
            with session.start_transaction():
                feature_db = self.client["feature"]
                self.__drop_collection(
                    db=feature_db, col_name="position"
                )  # Drop position collection
                self.__drop_collection(
                    db=feature_db, col_name="sensor"
                )  # Drop sensor collection
                position_col = feature_db[
                    "position"
                ]  # Recreate position collection (lazy)
                sensor_col = feature_db["sensor"]  # Recreate sensor collection (lazy)
                position_col.insert_many(metadata[0])  # Insert position documents
                sensor_col.insert_many(metadata[1])  # Insert sensor documents

    def _close_client(self):
        """

        :return:
        """
        if self.client is not None:
            self.client.close()

    @staticmethod
    def __drop_collection(db, col_name):
        """

        :param db:
        :param col_name:
        :return:
        """
        collection = db[col_name]
        flag = collection.drop()
        logger.info(f"Drop {col_name} collection result {flag}")
