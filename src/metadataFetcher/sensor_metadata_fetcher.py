"""
    A module for sensor and position metadata fetcher class (Concrete 1)
"""

from metadata_fetcher import MetadataFetcher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)


class SensorMetadataFetcher(MetadataFetcher):
    """Concrete #1 Class from 'MetadataFetcher'
    Sensor and Position Metadata Fetcher
     that connect to external data sources and fetch metadata as object"""

    def __get_or_create_session(self, conn_conf: object):
        """
        :return:
        """
        logger.debug("Entered '__get_or_create_session'")
        if self.session is None:
            # No exception handling so as to fail process
            logger.debug("Not yet has session")
            url = (
                f"mysql+pymysql://{conn_conf.user.id}:{conn_conf.user.pw}@"
                f"{conn_conf.addr}:{conn_conf.port}/{conn_conf.db}"
            )
            engine = create_engine(url, echo=True)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            logger.info("Session created: ", self.session)
        else:
            logger.debug("Already has session")
        return self.session

    def __get_jsonified_metadata(self):
        """

        :return:
        """
        return

    def _map_relational_to_object(self):
        """ORM Executor

        :return:
        """
