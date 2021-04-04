#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import sys
import socket
import struct

if __name__ == "__main__":

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    client_socket.connect(("127.0.0.1", 7890))
    time.sleep(1)
    msg = "Hello,world"
    msg_buf = bytes(msg, encoding="UTF-8")
    msg_len = len(msg_buf)

    print(msg_len)
    print(msg)

    msg_len_buf = msg_len.to_bytes(length=4, byteorder="big", signed=False)
    client_socket.sendall(msg_len_buf)
    client_socket.sendall(msg_buf)
    time.sleep(1)
    client_socket.close()
