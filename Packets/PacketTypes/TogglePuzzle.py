from Packets.PacketTypes.BasePacket import BasePacket
import Packets.PacketTypes.BasePacket as BP
from importlib import reload


class TogglePuzzle(BasePacket):
    """TCP packet describing state of the switch-puzzle. Identified by header 0x3130"""

    def __init__(self, data):
        reload(BP)
        super().__init__(data)

    def parse(self):
        # Part togglestates, part unknown
        # TODO: Break down this range further
        self.unknown = self.data[2:16]

        self.x_pos = int.from_bytes(self.data[16:20], 'little')
        self.y_pos = int.from_bytes(self.data[20:24], 'little')
        self.z_pos = int.from_bytes(self.data[24:28], 'little')

        self.theta_angle = int.from_bytes(self.data[28:30], 'little', signed=True)
        self.phi_angle = int.from_bytes(self.data[30:32], 'little', signed=True)

        # Still don't get this one, only has a value in the extremes of up/down
        self.extr_angle = int.from_bytes(self.data[32:34], 'little', signed=True)

        self.movedirection = self.data[34:36]

    def print(self):
        pkt_str = "tgl " + self.header_str
        pkt_str += self.unknown.hex() + " "
        pkt_str += self._pos_to_string((self.x_pos, self.y_pos, self.x_pos))
        pkt_str += self._angles_to_string((self.theta_angle, self.phi_angle, self.extr_angle))
        pkt_str += self._movedir_to_string(self.movedirection)

        print(pkt_str)

    # TODO: You should probably be able to specify multiple modification algorithms and trigger one based on cmd input
    def _mod_packet(self):
        pass
