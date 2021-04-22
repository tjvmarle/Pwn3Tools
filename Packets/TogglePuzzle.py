from PacketTypes import Packet


class TogglePuzzle(Packet):

    def __init__(self, data):
        super().__init__(data)

    def parse(self):
        # Part togglestates, part unknown
        # TODO: Break down this range further
        self.unknown = int.from_bytes(self.data[2:16], 'big')

        self.x_pos = int.from_bytes(self.data[16:20], 'big')
        self.y_pos = int.from_bytes(self.data[20:24], 'big')
        self.z_pos = int.from_bytes(self.data[24:28], 'big')

        # TODO: Translate to degrees (float, fixed with --> import struct)
        self.theta_angle = int.from_bytes(self.data[28:30], 'big')
        self.phi_angle = int.from_bytes(self.data[30:32], 'big')

        # Still don't get this one, some kind of overflow for up/down angle
        self.top_angle = int.from_bytes(self.data[32:34], 'big')

        self.movedirection = self.data[34:36]

    def print(self):
        packet_str = "tgl "

        for pos in (self.x_pos, self.y_pos, self.x_pos):
            packet_str += self.pos_to_string(pos)

        packet_str += self.angle_to_string(self.theta_angle)
        packet_str += self.angle_to_string(self.phi_angle)
        packet_str += hex(self.top_angle).rjust(6)
        packet_str += self.movedir_to_string(self.movedirection)

        print(packet_str)

    # TODO: You should probably be able to specify multiple modification algorithms and trigger one based one cmd input
    def mod(self):
        pass
