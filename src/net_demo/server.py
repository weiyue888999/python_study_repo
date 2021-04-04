#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import socket
import threading
import queue
import struct
import logging


class ClientHandler:


    def __init__(self, client_socket, addr,client_id,net_server):
        self.client_id = client_id 
        self.client_socket = client_socket
        self.client_socket.setblocking(True)
        self.addr = addr
        self.net_server = net_server

        logging.info("new client id={} :{}".format(self.client_id, addr))

        self.alive = True

        self.receive_msg_queue = queue.Queue(maxsize=8)
        self.send_msg_queue = queue.Queue(maxsize=8)

        self.read_thread = threading.Thread(
            target=ClientHandler.fun_read, args=(self,), name="read-thread"
        )
        self.write_thread = threading.Thread(
            target=ClientHandler.fun_write, args=(self,), name="write-thread"
        )

        self.read_thread.start()
        self.write_thread.start()

    def fun_read(self):
        logging.info("ReadThread-client_id={} start".format(self.client_id))
        while self.alive:
            len_buf = self.client_socket.recv(4)
            if not len_buf:
                break
            msg_len = int.from_bytes(len_buf, byteorder="big", signed=False)
            if msg_len < 0:
                logging.warn("msg len < 0")
            msg_buf = self.client_socket.recv(msg_len)
            msg = str(msg_buf, encoding="UTF-8")
            logging.debug(msg)

        self.alive = False
        logging.info("ReadThread-client_id={} stop".format(self.client_id))

        self.net_server.remove_client(self.client_id)

    def fun_write(self):
        logging.info("WriteThread-client_id={} start".format(self.client_id))
        while self.alive:
            try:
                msg = self.send_msg_queue.get(timeout=5)
                self.client_socket.send(msg)
            except queue.Empty:
                pass

        logging.info("WriteThread-client_id={} stop".format(self.client_id))

        self.net_server.remove_client(self.client_id)

    def write(self, msg):
        while self.alive:
            self.send_msg_queue.put(msg)

    def close():

        self.alive = False
        self.net_server.remove_client(self.client_id)

class NetServer:
    "server"

    next_client_id = 0

    def get_next_client_id():
        
        ret_val = NetServer.next_client_id
        NetServer.next_client_id += 1

        return ret_val

    def __init__(self, port):
        self.port = port
        self.alive = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.clients ={} 

    def startup(self):
        self.server_socket.bind(("127.0.0.1", self.port))
        self.server_socket.listen(16)

    def remove_client(self,client_id):
        if client_id in self.clients:
            del self.clients[client_id] 
            logging.debug("remove client client_id={}".format(client_id))

    def join(self):
        while self.alive:

            client_socket, addr = self.server_socket.accept()

            client_id = NetServer.get_next_client_id()
            self.clients[client_id] = ClientHandler(client_socket, addr,client_id,self)

    def shutdown(self):
        pass
