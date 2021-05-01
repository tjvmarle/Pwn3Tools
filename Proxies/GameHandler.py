import socket
from Proxies.BaseProxy import BaseProxy


class GameHandler(BaseProxy):
    """Handles the game-side part of the connection."""

    def __init__(self, port, host):
        super(GameHandler, self).__init__(port, host)
        self.name = "GH"
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind((self.host, self.port))

        # FIXME: Completion of the setup in main blocks here on unused handlers, move to own thread and run from there
        self.client.listen(1)
        self.client = self.client.accept()[0]  # Bit ugly, but it works
        self.connected = True
        print("Connected {}[{}]".format(self.name, self.port))
