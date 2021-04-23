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

serverPackets = {0x6d61: "mana"}

classMap = {
    0x6d76: Position,
    0x3031: TogglePuzzle,
}


class PacketManager():
    # Recieve packets from both sides. Instantiate respective classes

    def __init__(self):
        self.packet = None
        self.reciever = None
        # TODO: Add server and all the clients

    def print_unknown(self, data):
        packet_string = ""
        for byte in data:
            packet_string += byte.hex() + " "
        print("unk ", packet_string)

    def parse_packet(self, data, source):
        packetSource = gamePackets if source == "client" else serverPackets

        header = int.from_bytes(data[:2], "big")
        if header in packetSource:
            self.packet = packetSource[header](data)
        else:
            self.print_unknown(data)

        if self.reciever is not None:
            packet = data if not self.packet.modified else self.packet.new_packet
            self.reciever.sendall(packet)
