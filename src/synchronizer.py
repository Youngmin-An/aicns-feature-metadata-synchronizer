#!/usr/bin/env python
import click
import os
import logging
from synchronizerFactory import SensorSynchronizerFactory


def client():
    logger = logging.getLogger(__name__)
    logger.debug("Entered client")

    # Instantiate synchronizerFactory
    synchronizer_factory = SensorSynchronizerFactory()
    # Fetch metadata
    fetcher = synchronizer_factory.create_metadata_fetcher()
    source_conn_conf = __get_source_conn_conf()
    metadata = fetcher.fetch_metadata(source_conn_conf)
    logger.info(f"Metadata {metadata}")

    # Upsert metadata
    upserter = synchronizer_factory.create_metadata_upserter()
    dest_conn_conf = __get_dest_conn_conf()
    upserter.upsert_metadata(conn_conf=dest_conn_conf, metadata=metadata)
    upserter.close_client
    logger.info("Synchronizing success")


def __get_source_conn_conf():
    logger = logging.getLogger(__name__)
    logger.debug("Entered __get_source_conn_conf")
    conn_conf = dict()
    try:
        id = os.environ["SOURCE_USER_ID"]
        pw = os.environ["SOURCE_USER_PW"]
        conn_conf["user"] = {"id": id, "pw": pw}
        conn_conf["addr"] = os.environ["SOURCE_ADDRESS"]
        conn_conf["port"] = os.environ["SOURCE_PORT"]
        conn_conf["db"] = os.environ["SOURCE_DATABASE"]
    except Exception as e:
        logger.error(f"Can't read source env: {e}")
        raise e
    else:
        logger.info(f"Source conn_conf: {conn_conf}")
    return conn_conf


def __get_dest_conn_conf():
    logger = logging.getLogger(__name__)
    logger.debug("Entered __get_dest_conn_conf")
    conn_conf = dict()
    try:
        conn_conf["addr"] = os.environ["DESTINATION_ADDRESS"]
        conn_conf["port"] = os.environ["DESTINATION_PORT"]
    except Exception as e:
        logger.error(f"Can't read dest env: {e}")
        raise e
    else:
        logger.info(f"Dest conn_conf: {conn_conf}")
    return conn_conf


@click.command()
def main():
    client()
    pass


if __name__ == "__main__":
    log_level = os.environ.get("APP_LOG_LEVEL", "INFO")
    logging.basicConfig(level=log_level)
    main()
