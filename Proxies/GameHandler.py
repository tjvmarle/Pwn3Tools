import socket
from Proxies.BaseProxy import BaseProxy


class GameHandler(BaseProxy):
    """Handles the game-side part of the connection."""

    def __init__(self, port, host):
        super(GameHandler, self).__init__(port, host)
        self.name = "GH"
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.client = self.socket.accept()[0]
        self.connected = True
        print("Connected {}[{}]".format(self.name, self.port))
