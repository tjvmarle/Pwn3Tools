import socket
from threading import Thread
from Proxies.BaseProxy import BaseProxy


class ServerHandler(BaseProxy):
    """Handles the server-side part of the connection."""

    def __init__(self, port, host):
        super(ServerHandler, self).__init__(port, host)
        self.name = "SH"
        self.socket.connect((host, port))
        self.client = self.socket.accept()[0]
        self.connected = True
        print("Connected {}[{}]".format(self.name, self.port))
