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
        pkt_str = "tgl "

        pkt_str += self.__pos_to_string((self.x_pos, self.y_pos, self.x_pos))
        pkt_str += self.__angles_to_string((self.theta_angle, self.phi_angle))
        pkt_str += hex(self.top_angle).rjust(6)
        pkt_str += self.movedir_to_string(self.movedirection)

        print(pkt_str)

    # TODO: You should probably be able to specify multiple modification algorithms and trigger one based one cmd input
    def __mod_packet(self):
        pass
