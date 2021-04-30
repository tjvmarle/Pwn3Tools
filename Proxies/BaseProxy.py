import socket

class BaseProxy():
    """Core part of both the client- and server handler"""

    def __init__(self, port, host):
        self.crossref = None # Reference to other pair of the proxy
        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pm = None
        pass

    def setPacketManager(self, packetmanager):
        """
        Method to set a new PM. Ensures no references hang to CLI or other references get lost
            packetmanager: a new PacketManager object
        """
        if self.pm is not None:
            self.pm.stop_listening()
            packetmanager.receiver = self.pm.receiver
            packetmanager.generator = self.pm.generator

        self.pm = packetmanager

    def setCrossRef(self, xref):
        """Reference to the other side of the handler-pair"""
        self.crossref = xref 