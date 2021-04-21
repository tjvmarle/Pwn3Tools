class Packet():

    def __init__(self, data):
        self.data = data      # Recieved packet
        self.new_data = None  # Placeholder for modified packets
        self.parse()

    # Reverse Endianness except for the header (first two bytes)
    def reverse_endian(self, byte_string):
        # TODO: Implement in base
        pass

    # Print the packet to console in a formatted way
    def print(self):
        raise NotImplementedError()

    # Create a new packet based on the input
    def mod(self):
        raise NotImplementedError()

    # Convert packet to more meaningful data
    def parse(self):
        raise NotImplementedError()


class PositionPacket(Packet):

    def __init__(self, data):
        super().__init__(data)
        self.x_pos, self.y_pos, self.z_pos = 0, 0, 0

    def parse(self):
        self.x_pos = int.from_bytes(self.data[2:6], 'big')
        self.y_pos = int.from_bytes(self.data[6:10], 'big')
        self.z_pos = int.from_bytes(self.data[10:14], 'big')
        self.xz_angle = int.from_bytes(self.data[14:16], 'big')
        self.xy_angle = int.from_bytes(self.data[16:18], 'big')
        self.top_angle = int.from_bytes(self.data[18:20], 'big')
        self.movedirection = self.data[20:22]

    def print(self):
        pos_string = "pos "
        pos_string += str(self.x_pos).rjust(10)
        pos_string += str(self.y_pos).rjust(10)
        pos_string += str(self.z_pos).rjust(10)
        pos_string += str(self.xz_angle).rjust(6)
        pos_string += str(self.xy_angle).rjust(6)
        pos_string += hex(self.top_angle).rjust(6)
        first_byte = {0x00: "  ", 0x81: " L", 0x71: " R"}
        second_byte = {0x00: "  ", 0x81: " F", 0x71: " B"}

        pos_string += first_byte[self.movedirection[0]]
        pos_string += second_byte[self.movedirection[0]]

        print(pos_string)
