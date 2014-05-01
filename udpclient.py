import socket
import time

from easy_threading import FunctionThread, ServerBase


__author__ = 'Ruben Nielsen'


class UDPClient(ServerBase):
    MSGLEN = 2048

    def __init__(self, handle_function):
        super(UDPClient, self).__init__()
        self.handle = handle_function

        _handle = self.handle
        def input_threading():
            while 1:
                (message, address) = self.receive()
                # Handle each request in its own thread
                FunctionThread(handle, (message, address)).start()

        # Handle all requests in its own thread
        FunctionThread(input_threading).start()

if __name__ == '__main__':
    def handle(msg, addr):
        if msg == "Test":
            print "Awesome"
        else:
            print "Not awesome"

    server = ("127.0.0.1",8181)
    client = UDPClient(handle)
    client.send("JOIN", server)
    client.send("Test2", server)
    client.send("Test3", server)
    time.sleep(1)

