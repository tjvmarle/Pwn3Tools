from CLI import CommandListener
# from Packets.PacketTypes.Position import Position
# from Packets.PacketTypes.TogglePuzzle import TogglePuzzle

from importlib import reload
import Packets.PacketTypes.Position
import Packets.PacketTypes.TogglePuzzle


class PacketManager():
    """Handle the packets of one side of the proxy, so each proxy should get 2 PM's."""

    gamePackets = {
        0x6d76: Packets.PacketTypes.Position.Position,
        0x3031: Packets.PacketTypes.TogglePuzzle.TogglePuzzle,
        # 0x0000, : "heartbeat",
        # 0x6a70, : "jump",
        # 0x2a69, : "shoot", #inc. spells
        # 0x733d, : "wpn_switch",
    }

    serverPackets = {
        # 0x6d61: "mana"
    }

    # filter = (0x0000, 0x1703, 0x6d76)
    filter = (0x0000, 0x1703)

    def cmd(self, cmd_input):
        """
        This method will (eventually) implement all commands it should react to from the CLI
            cmd_input: list containing the CLI-command [0] and possible arguments [1:]
        """
        print("Cmd received:", cmd_input)

    def __init__(self, client, cli):
        # TODO: accept a Commandlistener, not a CLI
        """
        client: Signals if this PM handles either the game or the server (GH/SH)
        cli:    Reference to CLI to enable listening in on user input
        """

        # FIXME: Reloading the Packets-module doesn't seem to work here yet

        self.cmd_listener = CommandListener(cli, self.cmd)
        self.packet = None
        self.receiver = None  # The intended receiver of the packet
        self.client = client
        self.packetConfig = PacketManager.gamePackets if self.client == "GH" else PacketManager.serverPackets

    def __print_unknown(self, data, prefix):
        """
        Print a packet not defined in either dict
            data: raw bytes list
        """

        packet_string = ""
        alternator = False
        for byte in data:
            packet_string += format(byte, "x").rjust(2, "0") + (" " if alternator else "")
            alternator = not alternator
        print(prefix, end="")
        print("unk", packet_string)

    def handle_packet(self, data):
        """
        Entry function for the proxy the let the PM process an incoming packet
            data:   TCP packet in the form of a raw bytes list
        """

        header = int.from_bytes(data[:2], "big")
        prefix = "[{}]: ".format(self.client)

        if int.from_bytes(data[:2], "big") not in PacketManager.filter:
            if header in self.packetConfig:
                self.packet = self.packetConfig[header](data)
                print(prefix, end="")
                self.packet.print()
            else:
                self.__print_unknown(data, prefix)

        # Should be set most of the time:
        # try:
        #     self.generator.update(data)
        # except AttributeError:
        #     pass

        out_packet = None
        if self.packet is not None and self.packet.modified:
            out_packet = self.packet.new_packet
        else:
            out_packet = data

        # The PM als handles resending the packets, perhaps should be the responsibility of someone else
        if self.receiver is not None:
            self.receiver.sendall(out_packet)
            self.packet = None

        return out_packet

    # TODO: First implement the generator itself more before you hang it everywhere
    # def set_generator(self, generator):
    #     self.generator = generator

    # def inject(self, packet_type):
    #     for packet in self.generator.generate(packet_type):
    #         self.receiver.sendall(packet)
