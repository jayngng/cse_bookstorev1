#!/usr/bin/env python3

import threading
from pwn import listen

class NetCat:
    def __init__(self, port):
        self.port = port

    def listener(self):
        nc = listen(self.port)
        nc.wait_for_connection()
        nc.interactive()

    def start(self):
        run = threading.Thread(target=self.listener)
        run.start()

if __name__=='__main__':
    nc = NetCat(9999)
    nc.start()

