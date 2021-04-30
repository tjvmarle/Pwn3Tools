import socket
from threading import Thread
from Proxies.BaseProxy import BaseProxy

class GameHandler(Thread, BaseProxy):
    """Handles the game-side part of the connection."""
    
    def __init__(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        
        self.client = self.socket.accept()[0]
        self.connected = True
        print("Connected GH[{}]".format(self.port))
        pass

    def run(self):
        #TODO: Miss hier pas zetten dat de PM "game"/"server" is?
        while True:
            data = self.client.recv(4096)
            if data:
                try:
                    self.pm.handle_packet(data)

                except Exception as e:
                    print("client[{}] error: ".format(self.port), e)
        pass