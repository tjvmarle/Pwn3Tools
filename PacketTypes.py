class Packet():

    def __init__(self, data):
        self.data = data      # Recieved packet
        self.new_data = None  # Placeholder for modified packets

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
