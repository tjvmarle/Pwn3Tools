import socket
import os
from threading import Thread
from importlib import reload

from Packets.PacketManager import PacketManager
from Packets.PacketGenerator import Generator as PG
# from Packets.PacketGenerator import Generator
from CLI import CommandLineInput


# Basic proxy setup shamelessly stolen from LiveOverflow
class Proxy2Server(Thread):
    """Client Proxy to handle incoming data from the Master- and Gameservers"""

    def set_packet_manager(self, new_pm):
        """
        Method to set a new PM. Ensures no references hang to CLI or other references get lost
            new_pm: a new PacketManager object
        """
        if self.pm is not None:
            self.pm.stop_listening()
            new_pm.receiver = self.pm.receiver
            new_pm.generator = self.pm.generator

        self.pm = new_pm

    def __init__(self, host, port, cli):
        super(Proxy2Server, self).__init__()
        self.game = None  # Reference to other proxy
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self.pm = PacketManager("server", cli)
        # self.pm.set_generator(PG.Generator)

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

    # TODO: Refactor this into a base proxy class so you can get rid of this duplicate code
    def set_packet_manager(self, new_pm):
        """
        Method to set a new PM. Ensures no references hang to CLI or other references get lost
            new_pm: a new PacketManager object
        """
        if self.pm is not None:
            self.pm.stop_listening()
            new_pm.receiver = self.pm.receiver
            new_pm.generator = self.pm.generator

        self.pm = new_pm

    def __init__(self, host, port, cli):
        super(Game2Proxy, self).__init__()
        self.server = None  # Reference to other proxy
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)

        # waiting for a connection
        self.game = sock.accept()[0]  # This is were the thread will block if not used!
        self.connected = False

        self.pm = PacketManager("client", cli)
        # self.pm.set_generator(PG.Generator)

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

    def __init__(self, from_host, to_host, port, cli):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
        self.running = False
        self.cli = cli

    def run(self):
        # while True: #I don't think this one is actually necessary...

        self.g2p = Game2Proxy(self.from_host, self.port, self.cli)
        self.p2s = Proxy2Server(self.to_host, self.port, self.cli)

        # Cross-references for the packetmanager
        self.g2p.pm.receiver = self.p2s.server
        self.p2s.pm.receiver = self.g2p.game

        self.g2p.start()
        self.p2s.start()
        self.running = True

    def reset_pm(self):
        pass


CLI = CommandLineInput()

# First boot al servers
SERVER_ADDRESS = "192.168.138.130"  # Set to IP of Ubuntu VM

master_server = Proxy('0.0.0.0', SERVER_ADDRESS, 3333, CLI)
master_server.start()
print("Listening on: {}".format(SERVER_ADDRESS + ":" + str(3333)))

game_servers = []
for port in range(3000, 3006):
    _game_server = Proxy('0.0.0.0', SERVER_ADDRESS, port, CLI)
    _game_server.start()
    game_servers.append(_game_server)
    print("Listening on: {}".format(SERVER_ADDRESS + ":" + str(port)))


def reload_proxies():
    # receiver and generator needs to be preserved
    for entry in game_servers:

        if not entry.running:
            continue

        #TODO: cleanup
        entry.g2p.set_packet_manager(PacketManager("client", CLI))
        entry.p2s.set_packet_manager(PacketManager("server", CLI))

        # old_pm_cl = entry.g2p.pm
        # new_pm_cl = PM.PacketManager("client")
        # new_pm_cl.receiver = old_pm_cl.receiver
        # new_pm_cl.generator = old_pm_cl.generator
        # entry.g2p.pm = new_pm_cl

        # old_pm_sr = entry.p2s.pm
        # new_pm_sr = PM.PacketManager("server")
        # new_pm_sr.receiver = old_pm_sr.receiver
        # new_pm_sr.generator = old_pm_sr.generator
        # entry.p2s.pm = new_pm_sr
        print("\nReloaded", entry.g2p.port, "\n\n\n")


# Loop for user input
while True:
    try:
        cmd = input()

        if cmd[:4] == 'quit':
            os._exit(0)

        else:
            reload(PacketManager)
            reload_proxies()

    except Exception as e:
        print("Error in command-loop: ", e)
