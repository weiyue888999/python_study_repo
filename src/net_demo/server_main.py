#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import socket
import server
import logging

if __name__ == "__main__":

    logging.basicConfig(
        format="%(levelname)s:%(asctime)s:%(message)s", level=logging.DEBUG
    )
    logging.info("startup")

    netServer = server.NetServer(7890)
    netServer.startup()
    netServer.join()
    netServer.shutdown()

    logging.info("shutdown")
