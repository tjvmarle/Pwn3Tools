import socket
from threading import Thread


class BaseProxy(Thread):
    """Core part of both the client and server handler"""

    def __init__(self, port, host):
        super(BaseProxy, self).__init__()
        self.crossref = None  # Reference to other pair of the proxy
        self.port = port
        self.host = host
        self.client = None

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pm = None
        self.name = ""

    def setPacketManager(self, new_pm):
        """
        Method to set a new PM. Ensures no references hang to CLI or other references get lost.
            packetmanager: a new PacketManager object
        """
        if self.pm is not None:
            self.pm.cmd_listener.stop_listening()
            new_pm.client = self.pm.client
            # new_pm.generator = self.pm.generator

        self.pm = new_pm

    # TODO: Apparently getters/setters are not 'pythonic'. Check out alternative.
    def setCrossRef(self, xref):
        """
        Reference to the other side of the handler-pair.
            xref: Reference to the other instance
        """
        self.crossref = xref

    def pre_run_check(self):
        """Couple of selfchecks before runnning this side of the proxy."""
        runnable = True

        if self.name == "":
            self.name = "Unknown"
            print("{}[{}]Name missing".format(self.name, self.port))
            runnable = False
        prefix = ("{}[{}]".format(self.name, self.port))

        if self.client is None:
            print(prefix + "Client missing")
            runnable = True

        if self.crossref == None:
            print(prefix + "Crossreference missing")
            runnable = True

        if self.pm == None:
            print(prefix + "PacketManager missing")
            runnable = True

        if not runnable:
            print(prefix + "Aborting startup")

        return runnable

    def run(self):
        runnable = self.pre_run_check()
        print("Running {}[{}]".format(self.name, self.port))
        while runnable:
            data = self.client.recv(4096)
            if data and self.pm is not None:
                try:
                    new_data = self.pm.handle_packet(data)
                    for packet in new_data:
                        self.crossref.client.sendall(packet)

                except Exception as e:
                    print("{}[{}] error: ".format(self.name, self.port), e)
