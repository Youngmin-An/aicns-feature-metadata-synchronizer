"""
    A module for sensor and position metadata fetcher class (Concrete 1)
"""

from metadataFetcher import MetadataFetcher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from objects.sensor import SensorType, SensorPos, SensorManage

import logging

logger = logging.getLogger(__name__)


class SensorMetadataFetcher(MetadataFetcher):
    """Concrete #1 Class from 'MetadataFetcher'
    Sensor and Position Metadata Fetcher
     that connect to external data sources and fetch metadata as object"""

    def _get_or_create_session(self, conn_conf: object):
        """
        :return:
        """
        logger.debug("Entered '__get_or_create_session'")
        if self.session is None:
            # No exception handling so as to fail process
            logger.debug("Not yet has session")
            url = (
                f"mysql+pymysql://{conn_conf['user']['id']}:{conn_conf['user']['pw']}@"
                f"{conn_conf['addr']}:{conn_conf['port']}/{conn_conf['db']}"
            )
            engine = create_engine(url, echo=True)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            logger.info(f"Session created: {self.session}")
        else:
            logger.debug("Already has session")
        return self.session

    def _get_dictionary_metadata(self):
        """

        :return:
        """
        positions = self.__get_dictionary_positions()
        sensors = self.__get_dictionary_sensors()
        return positions, sensors

    def __get_dictionary_positions(self):
        """Map ORM sensor positions and Transform as list of dictionary

        :return:
        """
        logger.debug("Entered __get_dictionary_positions")
        positions = self.session.query(SensorPos).all()
        wanted_keys = {"pos_id", "pos_code", "pos_name", "pos_dtl"}
        dict_positions = list(map((lambda pos: pos.__dict__), positions))
        filtered_positions = list(
            map((lambda pos: {key: pos[key] for key in wanted_keys}), dict_positions)
        )
        logger.info(f"fetched dictionary positions: {filtered_positions}")
        return filtered_positions

    def __get_dictionary_sensors(self):
        """Map ORM Sensor metadata, Join them and Transform as list of dictionary

        :return:
        """
        logger.debug("Entered __get_dictionary_sensors")
        join_sources = (
            self.session.query(SensorManage, SensorPos, SensorType)
            .filter(SensorManage.sensorpos_id == SensorPos.pos_id)
            .filter(SensorManage.sensortype_id == SensorType.type_id)
            .all()
        )
        sensors = []
        for join_rows in join_sources:
            dict_sensor = self.__sensor_object_to_dictionary(join_rows[0])
            dict_position = self.__sensor_object_to_dictionary(join_rows[1])
            dict_type = self.__sensor_object_to_dictionary(join_rows[2])
            dict_sensor["position"] = dict_position
            dict_sensor["type"] = dict_type
            sensors.append(dict_sensor)
        logger.info(f"joined sensor dictionary: {sensors}")
        return sensors

    @staticmethod
    def __sensor_object_to_dictionary(object):
        """Util method for transforming object to dictionary

        :param object: Target object
        :return: A dictionary that execluded some unwanted properties
        """
        unwanted_keys = {"_sa_instance_state", "sensorpos_id", "sensortype_id"}
        raw_dictionary = object.__dict__
        dictionary = {
            key: raw_dictionary[key]
            for key in raw_dictionary
            if key not in unwanted_keys
        }
        return dictionary
