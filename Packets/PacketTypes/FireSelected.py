from Packets.PacketTypes.BasePacket import BasePacket
import Packets.PacketTypes.BasePacket as BP
from importlib import reload


class FireSelected(BasePacket):
    """TCP packet describing the player firing a weapon or casting a spell. Identified by header 0x2a69"""

    def __init__(self, data):
        reload(BP)
        super().__init__(data)

    def parse(self):
        # This works for the handgun, maybe not for everything else.
        self.x_pos = int.from_bytes(self.data[24:28], 'little')
        self.y_pos = int.from_bytes(self.data[28:32], 'little')
        self.z_pos = int.from_bytes(self.data[32:36], 'little')
        self.theta_angle = int.from_bytes(self.data[36:38], 'little', signed=True)
        self.phi_angle = int.from_bytes(self.data[38:40], 'little', signed=True)
        self.extr_angle = int.from_bytes(self.data[40:42], 'little', signed=True)
        self.movedirection = self.data[42:44]

    def print(self):
        pos_str = "fir " + self.header_str

        cntr = 2
        for byte in self.data[2:24]:
            pos_str += format(byte, "x").rjust(2, "0")
            cntr -= 1
            if cntr == 0:
                cntr = 4
                pos_str += " "

        pos_str += self._pos_to_string((self.x_pos, self.y_pos, self.z_pos))
        pos_str += self._angles_to_string((self.theta_angle, self.phi_angle, self.extr_angle))
        pos_str += self._movedir_to_string(self.movedirection)

        print(pos_str)

    def _mod_packet(self):
        pass
