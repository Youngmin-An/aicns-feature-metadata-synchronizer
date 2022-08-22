"""
    Test scripts for instantiated metadta_fetcher by sensor_metadata_fetcher
"""
import sys

sys.path.append("../../src")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.objects.common_base import Base
from src.objects.sensor import SensorPos, SensorType, SensorManage
from src.metadataFetcher import MetadataFetcher, SensorMetadataFetcher


class TestSensorMetadataFetcher:
    @pytest.fixture
    def session(self, connection):
        """

        :param connection:
        :return:
        """
        transaction = connection.begin()
        Session = sessionmaker()
        session = Session(bind=connection)
        yield session
        session.close()
        transaction.rollback()

    @pytest.fixture(scope="module", autouse=True)
    def set_up_db(self, engine):
        """

        :param engine:
        :return:
        """
        SensorPos.metadata.create_all(engine)
        SensorType.metadata.create_all(engine)
        SensorManage.metadata.create_all(engine)

    @pytest.fixture(scope="module")
    def connection(selfslef, engine):
        """

        :param engine:
        :return:
        """
        connection = engine.connect()
        yield connection
        connection.close()

    @pytest.fixture(scope="module")
    def engine(self):
        """

        :return:
        """
        return create_engine("sqlite:///:memory:")

    def test_fetch_metadata(
        self,
        session,
    ):
        # Given (Scenario #1)
        session.add(
            SensorPos(pos_id=1, pos_code="CD", pos_dtl="A street", pos_name="CD"),
            SensorPos(pos_id=3, pos_code="AB", pos_dtl="B street", pos_name="AB"),
        )
        session.add(
            SensorType(
                type_id=2,
                type_code="T",
                type_color_code="#f44336",
                type_name="Temperature",
                unit="ºC",
            )
        )
        session.add(
            SensorManage(
                ss_id=4,
                rstart=0.0,
                rlev1=0.0,
                rlev2=0.0,
                rlev3=0.0,
                rlev4=0.0,
                rend=0.0,
                sensorpos_id=1,
                sensortype_id=2,
            )
        )
        session.commit()
        fetcher: MetadataFetcher = SensorMetadataFetcher(session)

        # When (Scenario #1)
        positions, joined_sensors = fetcher.fetch_metadata({})

        expected_positions = [
            {"pos_id": 1, "pos_code": "CD", "pos_dtl": "A street", "pos_name": "CD"},
            {"pos_id": 3, "pos_code": "AB", "pos_dtl": "B street", "pos_name": "AB"},
        ]

        len_expected_sensors = 1
        # Then (Scenario #1)
        assert [i for i in positions if i not in expected_positions] == []
        assert len(joined_sensors) == len_expected_sensors
