from threading import Thread
from Proxies.GameHandler import GameHandler as GH
from Proxies.ServerHandler import ServerHandler as SH
from Packets.PacketManager import PacketManager as PM


class PwnProxy(Thread):
    def __init__(self, port, host, pmMap, cli):
        super(PwnProxy, self).__init__()
        self.port = port
        self.host = host
        self.pmMap = pmMap
        self.cli = cli
        self.gamehandler = None
        self.serverhandler = None

    def setPacketManagers(self, pmMap):
        # TODO: Isn't this a tad too convoluted? Maybe change into 'createPacketManagers' or something. Can probably be
        # deleted if both handlers are injected in constructor (PM's can be set beforehand then).
        self.gamehandler.setPacketManager(pmMap["GH"])
        self.serverhandler.setPacketManager(pmMap["SH"])

    def resetPacketManagers(self):
        self.gamehandler.setPacketManager(PM("GH", self.cli))
        self.serverhandler.setPacketManager(PM("SH", self.cli))

    def run(self):
        # Should probably accept these as arguments in the constructor for better dependency inj.
        self.gamehandler = GH(self.port, "0.0.0.0")
        self.serverhandler = SH(self.port, self.host)

        self.setPacketManagers(self.pmMap)  # TODO: Bit ugly, find something more aesthetic

        self.gamehandler.setCrossRef(self.serverhandler)
        self.serverhandler.setCrossRef(self.gamehandler)

        self.gamehandler.start()
        self.serverhandler.start()
