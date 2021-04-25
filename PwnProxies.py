import socket
import os
from threading import Thread
import proxyparser as parser
# import random
# import struct
from importlib import reload
import PacketManager as PM
from PacketGenerator import Generator


# Basic proxy setup shamelessly stolen from LiveOverflow
class Proxy2Server(Thread):
    """Client Proxy to handle incoming data from the Master- and Gameservers"""

    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.game = None
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self.pm = PM.PacketManager("server")
        self.pm.set_generator(Generator)

    def run(self):
        while True:
            data = self.server.recv(4096)

            if data:
                try:
                    self.pm.handle_packet(data)

                except Exception as e:
                    print('server[{}] error: '.format(self.port), e)


class Game2Proxy(Thread):
    """Server Proxy to handle incoming data from the Client (the game)"""

    def __init__(self, host, port):
        super(Game2Proxy, self).__init__()
        self.server = None  # Reference to other proxy
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)

        # waiting for a connection
        self.game, addr = sock.accept()
        self.connected = False

        self.pm = PM.PacketManager("client")

    def run(self):
        while True:
            data = self.game.recv(4096)
            if data:
                self.connected = True
                try:
                    self.pm.handle_packet(data)

                except Exception as e:
                    print("client[{}] error: ".format(self.port), e)


class Proxy(Thread):

    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
        # self.running = False

    def run(self):
        while True:

            self.g2p = Game2Proxy(self.from_host, self.port)
            self.p2s = Proxy2Server(self.to_host, self.port)

            # Cross-referencing both proxies to forward packets
            # self.g2p.server = self.p2s.server
            # self.p2s.game = self.g2p.game
            # self.running = True

            # Same references for the packetmanager
            self.g2p.pm.reciever = self.p2s.server
            self.p2s.pm.reciever = self.g2p.game

            self.g2p.start()
            self.p2s.start()


# First boot al servers
SERVER_ADDRESS = "192.168.138.130"  # Set to IP of Ubuntu VM

master_server = Proxy('0.0.0.0', SERVER_ADDRESS, 3333)
master_server.start()
print("Listening on: {}".format(SERVER_ADDRESS + ":" + str(3333)))

game_servers = []
for port in range(3000, 3006):
    _game_server = Proxy('0.0.0.0', SERVER_ADDRESS, port)
    _game_server.start()
    game_servers.append(_game_server)
    print("Listening on: {}".format(SERVER_ADDRESS + ":" + str(port)))

# Loop for user input
while True:
    try:
        cmd = input()

        if cmd[:4] == 'quit':
            os._exit(0)

        # elif cmd[:6] == 'inject':
        #     parser.inject(game_servers)

        else:
            # reload(PM)
            # TODO: After reloading, reinstantiate the PM's and reassign them. Don't forget to copy the pm.reciever's!
            # parser.execute(cmd)
            print("\n\n\nReloaded PacketManager\n\n\n")

    except Exception as e:
        print("Error in command-loop: ", e)
