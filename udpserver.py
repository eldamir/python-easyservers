import socket

from easy_threading import FunctionThread, ServerBase


__author__ = 'Ruben Nielsen'


class UDPServer(ServerBase):
    """
    A server for receiving messages and responding to them.
    """
    sock = None
    MSGLEN = 2048

    def __init__(self, handle_function, port=8181, threaded=True):
        """
        Creates a simple I/O server. The server handles incoming messages and
        may respond to them afterwards. The servers behaviour is controlled by
        the function passed to handle_function. The only behaviour that is
        predetermined is that the server uses UDP and only sends messages in
        response to received messages.
        The handle_function must accept the following parameters:
         * message - The message received by the server
         * address - The address from which the message was received
         * send    - The servers function for sending data back to the address

        :param handle_function: The function for handling messages
        :param port: The port number to create a socket on
        :param threaded: If True, incoming messages will be handled in their own thread
        """
        super(UDPServer, self).__init__()
        self.threaded = threaded
        self.port = port
        self.handle = handle_function
        self.hostname = "0.0.0.0"  # socket.gethostname()

        print("Setting up server")
        # Bind the socket to a public host,
        # and a well-known port
        self.sock.bind((self.hostname, self.port))

    def run(self):
        print("Server running on %s:%d" % (self.hostname, self.port))
        while 1:
            # Accept connections from outside
            (message, address) = self.receive()

            # If the server is threaded, start a new thread for handling the
            # message. Otherwise just handle the message in this thread
            if self.threaded:
                FunctionThread(self.handle, (message, address, self.send)).start()
            else:
                self.handle(message, address, self.send)

if __name__ == '__main__':
    # Simple echo server example
    def echo(msg, addr, send):
        print(msg)
        send(msg, addr)

    server = UDPServer(echo, threaded=True)
    server.run()