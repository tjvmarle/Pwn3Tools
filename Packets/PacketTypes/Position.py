from Packets.PacketTypes.BasePacket import BasePacket
import Packets.PacketTypes.BasePacket as BP
from importlib import reload


class Position(BasePacket):
    """TCP packet describing player position. Identified by header 0x6d76"""

    def __init__(self, data):
        reload(BP)
        super().__init__(data)

    def parse(self):
        self.x_pos = int.from_bytes(self.data[2:6], 'little')
        self.y_pos = int.from_bytes(self.data[6:10], 'little')
        self.z_pos = int.from_bytes(self.data[10:14], 'little')
        self.theta_angle = int.from_bytes(self.data[14:16], 'little', signed=True)
        self.phi_angle = int.from_bytes(self.data[16:18], 'little', signed=True)
        self.extr_angle = int.from_bytes(self.data[18:20], 'little', signed=True)
        self.movedirection = self.data[20:22]

    def print(self):
        pos_str = "pos " + self.header_str
        pos_str += self._pos_to_string((self.x_pos, self.y_pos, self.z_pos))
        pos_str += self._angles_to_string((self.theta_angle, self.phi_angle, self.extr_angle))
        pos_str += self._movedir_to_string(self.movedirection)

        print(pos_str)

    def _mod_packet(self):
        pass
