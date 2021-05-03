from Packets.PacketTypes.BasePacket import BasePacket
import Packets.PacketTypes.BasePacket as BP
from importlib import reload


class Mana(BasePacket):
    """TCP packet describing player mana and active spell projectiles. Identified by header 0x6d61"""

    def __init__(self, data):
        reload(BP)
        super().__init__(data)

    def parse(self):
        # Launching a projectile creates a single packet with higher length, probably describing the position + angle.
        # Following packets are shorter, probably containing positon modifications (angle will be unchanged). Firing
        # multiple projectiles leads to longer packets, as all projectiles are tracked in the same packet.
        # Base mana regen packet: 8 bytes
        # Each additional projectile is 24 bytes

        self.mana = int.from_bytes(self.data[2:3], 'little')

        # self._mod_packet()

    def print(self):
        if len(self.data) > 30:
            pos_str = "mana " + self.header_str
            pos_str += str(self.mana).rjust(3) + " "

            cntr = 4
            for byte in self.data[5:]:
                pos_str += format(byte, "x").rjust(2, "0")
                cntr -= 1
                if cntr == 0:
                    cntr = 4
                    pos_str += " "

            print(pos_str + "[{}]".format(str(len(self.data))))

    def _mod_packet(self):
        self.new_data = bytearray(self.data[:8])
        # self.new_data[2] = 100
        self.modified = True
