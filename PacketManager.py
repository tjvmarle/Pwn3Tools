from Packets import Position
from Packets import TogglePuzzle

gamePackets = {
    0x6d76: Position,
    0x3031: TogglePuzzle,
    # 0x0000, : "heartbeat",
    # 0x6a70, : "jump",
    # 0x2a69, : "spell",
    # 0x733d, : "wpn_switch",
}

serverPackets = {
    # 0x6d61: "mana"
}


class PacketManager():
    """Handle the packets of one side of the proxy, so each proxy should get 2 PM's."""

    def __init__(self):
        self.packet = None
        self.reciever = None

    def __print_unknown(self, data):
        """
        Print a packet not defined in either dict
            data: raw bytes list
        """

        packet_string = ""
        for byte in data:
            packet_string += byte.hex() + " "
        print("unk ", packet_string)

    def parse_packet(self, data, source):
        """
        Entry function for the proxy the let the PM process an incoming packet
            data:   TCP packet in the form of a raw bytes list
            source: source of the packet. Either 'client' or 'server'
        """

        packetSource = gamePackets if source == "client" else serverPackets

        header = int.from_bytes(data[:2], "big")
        if header in packetSource:
            self.packet = packetSource[header](data)
        else:
            self.__print_unknown(data)

        if self.reciever is not None:
            packet = data if not self.packet.modified else self.packet.new_packet
            self.reciever.sendall(packet)
