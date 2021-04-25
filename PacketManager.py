import Packets as TCP

gamePackets = {
    0x6d76: TCP.Position,
    0x3031: TCP.TogglePuzzle,
    # 0x0000, : "heartbeat",
    # 0x6a70, : "jump",
    # 0x2a69, : "spell",
    # 0x733d, : "wpn_switch",
}

serverPackets = {
    # 0x6d61: "mana"
}

filter = (0x0000, 0x1703, 0x6d76)


class PacketManager():
    """Handle the packets of one side of the proxy, so each proxy should get 2 PM's."""

    def __init__(self, source):
        """source: Signals if this PM recieves from either client or server """

        self.packet = None
        self.reciever = None  # The intended reciever of the packet
        self.source = source
        self.packetSource = gamePackets if self.source == "client" else serverPackets

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
        print("unk ", packet_string)

    def handle_packet(self, data):
        """
        Entry function for the proxy the let the PM process an incoming packet
            data:   TCP packet in the form of a raw bytes list
        """

        header = int.from_bytes(data[:2], "big")
        prefix = "[game]: " if self.source == "client" else "[serv]: "

        if int.from_bytes(data[:2], "big") not in filter:
            if header in self.packetSource:
                self.packet = self.packetSource[header](data)
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
        if self.reciever is not None:
            self.reciever.sendall(out_packet)
            self.packet = None

    def set_generator(self, generator):
        self.generator = generator

    def inject(self, packet_type):
        for packet in self.generator.generate(packet_type):
            self.reciever.sendall(packet)
