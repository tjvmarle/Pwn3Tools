from Proxies.GameHandler import GameHandler as GH
from Proxies.ServerHandler import ServerHandler as SH
from Packets.PacketManager import PacketManager as PM

class PwnProxy():
    def __init__(self, port, host, cli):
        self.gamehandler = GH(port, "0.0.0.0") #Should probably accept these too as arguments for better dependency inj.
        self.serverhandler = SH(port, host)
        self.cli = cli

        self.gamehandler.setCrossRef(self.serverhandler)
        self.serverhandler.setCrossRef(self.gamehandler)

    def setPacketManagers(self, pmMap):
        #TODO: Isn't this a tad too convoluted? Maybe change into 'createPacketManagers' or something. Can probably be
        # deleted if both handlers are injected in constructor (PM's can be set beforehand then). 
        self.gamehandler.setPacketManager(pmMap["GH"])
        self.serverhandler.setPacketManager(pmMap["SH"])

    def resetPacketManagers(self):
        self.gamehandler.setPacketManager(PM("GH", self.cli))
        self.serverhandler.setPacketManager(PM("SH", self.cli))

    def start(self):
        self.gamehandler.start()
        self.serverhandler.start()