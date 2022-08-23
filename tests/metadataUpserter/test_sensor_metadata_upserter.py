"""
    Test scripts for instantiated metadta_fetcher by sensor_metadata_fetcher
"""
import os
import sys

sys.path.append("../../src")

import pytest
from src.metadataUpserter import MetadataUpserter, SensorMetadataUpserter
from pymongo_inmemory import MongoClient


class TestSensorMetadataUpserter:
    @pytest.fixture(scope="function", autouse=False)
    def test_client(self):
        client = MongoClient()
        yield client
        client.close()

    @pytest.fixture(autouse=True)
    def pymongoim_os_env(self):
        if os.environ.get("PYMONGOIM__MONGOD_PORT") is None:
            os.environ["PYMONGOIM__MONGOD_PORT"] = "32154"
        if os.environ.get("PYMONGOIM__OPERATING_SYSTEM") is None:
            os.environ["PYMONGOIM__OPERATING_SYSTEM"] = "ubuntu"
        if os.environ.get("PYMONGOIM__OS_VERSION") is None:
            os.environ["PYMONGOIM__OS_VERSION"] = "18"
        yield
        # os.environ.pop("PYMONGOIM__MONGOD_PORT")
        # os.environ.pop("PYMONGOIM__OPERATING_SYSTEM")
        # os.environ.pop("PYMONGOIM__OS_VERSION")

    @pytest.fixture(scope="session", autouse=False)
    def positions(self):
        yield [
            {"pos_id": 1, "pos_code": "CD", "pos_dtl": "A street", "pos_name": "CD"},
            {"pos_id": 3, "pos_code": "AB", "pos_dtl": "B street", "pos_name": "AB"},
        ]

    @pytest.fixture(scope="session", autouse=False)
    def sensors(self):
        yield [
            {
                "rstart": 0.0,
                "rlev2": 0.0,
                "rlev3": 0.0,
                "rlev5": None,
                "rlev7": None,
                "rend": 0.0,
                "range_type": None,
                "rlev1": 0.0,
                "rlev4": 0.0,
                "rlev6": None,
                "rlev8": None,
                "ss_id": 4,
                "position": {
                    "pos_code": "CD",
                    "pos_dtl": "A street",
                    "pos_name": "CD",
                    "pos_id": 1,
                },
                "type": {
                    "type_code": "T",
                    "type_name": "Temperature",
                    "unit": "ºC",
                    "type_id": 2,
                    "type_color_code": "#f44336",
                },
            }
        ]

    def test_no_exception_when_db_does_not_exist(self, test_client, positions, sensors):
        # Given (Scenario 1)
        dbs = test_client.list_database_names()
        metadata = (positions, sensors)
        upserter: MetadataUpserter = SensorMetadataUpserter(client=test_client)
        # Then (Scenario 1)
        assert "feature" not in dbs

        # When (Scenario 1)
        try:
            upserter.upsert_metadata(conn_conf=None, metadata=metadata)
        # Then (Scenario 1)
        except Exception as e:
            pytest.fail(f"Fail, exception occurred in Scenario 1: {e}")

    def test_no_exception_when_collection_already_exist(self, test_client, positions, sensors):
        # Given (Scenario 2)
        metadata = (positions, sensors)
        temp_position =  {"pos_id": 7, "pos_code": "XX", "pos_dtl": "X street", "pos_name": "YY"}
        test_client["feature"]["position"].insert(temp_position)
        upserter: MetadataUpserter = SensorMetadataUpserter(client=test_client)

        # When (Scenario 2)
        try:
            upserter.upsert_metadata(conn_conf=None, metadata=metadata)
        # Then (Scenario 2)
        except Exception as e:
            pytest.fail(f"Fail, exception occured in Scenario 2: {e}")
        assert test_client["feature"]["position"].count() == 2
        assert test_client["feature"]["sensor"].count() == 1


    def test_upsert_metadata(self, test_client, positions, sensors):
        # Given (Scenario 3)
        metadata = (positions, sensors)
        upserter: MetadataUpserter = SensorMetadataUpserter(client=test_client)

        # When (Scenario 3)
        upserter.upsert_metadata(conn_conf=None, metadata=metadata)

        # Then (Scenario 3)
        # sensor = test_client["feature"]["sensor"].find_one({"type": {"type_code" : "T"}})
        sensor = test_client["feature"]["sensor"].find_one({"ss_id": 4})
        assert sensor["type"]["type_code"] == "T"
