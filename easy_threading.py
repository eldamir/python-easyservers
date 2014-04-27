__author__ = 'ruben'

import threading, socket


class FunctionThread(threading.Thread):
    def __init__(self, function, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        # Allow parent thread to execute this one
        self.daemon = True

    def run(self):
        self.function(*self.args, **self.kwargs)


class ServerBase(object):
    def __init__(self):
        # Create an INET, Datagram socket (UDP)
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

    def send(self, msg, address):
        self.sock.sendto(msg, address)

    def receive(self):
        (message, address) = self.sock.recvfrom(self.MSGLEN)
        return (message, address)

    def create_thread(self, function, args=[], kwargs={}, start=True):
        new_thread = FunctionThread(function, args, kwargs)
        if start:
            new_thread.start()
        return new_thread