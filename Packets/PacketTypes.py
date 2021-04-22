# Base class to parse the game packets.
# TODO: there should probably be some kind of packet_manager that takes care of instantiating the right subclass
class Packet():
    # TODO: check how 'correct' python commenting looks like

    def __init__(self, data):
        self.data = data      # Recieved packet
        self.new_data = None  # Placeholder for modified packets
        self.parse()

    # Reverse Endianness of the string
    def reverse_endian(self, byte_string):
        rev_string = ""

        # There's probably a more 'pythonic' way to do this
        while len(byte_string) > 0:
            rev_string += byte_string[-2:]
            byte_string = byte_string[:-2]

        return rev_string

    # Convert packet to more meaningful data
    def parse(self):
        raise NotImplementedError()

    # Print the packet to console in a formatted way
    def print(self):
        raise NotImplementedError()

    # Create a new packet based on the input
    def mod(self):
        raise NotImplementedError()
