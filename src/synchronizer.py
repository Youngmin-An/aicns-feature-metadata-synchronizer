#!/usr/bin/env python
import click
import os
import logging
from synchronizerFactory import SensorSynchronizerFactory


def client(conn_conf):
    logger = logging.getLogger(__name__)
    logger.debug("Entered client")
    synchronizer = SensorSynchronizerFactory()
    fetcher = synchronizer.create_metadata_fetcher()
    metadata = fetcher.fetch_metadata(conn_conf)
    logger.info(f"Metadata {metadata}")


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


@click.command()
def main():
    source_conn_conf = __get_source_conn_conf()
    client(source_conn_conf)
    pass


if __name__ == "__main__":
    log_level = os.environ.get("APP_LOG_LEVEL", "INFO")
    logging.basicConfig(level=log_level)
    main()
