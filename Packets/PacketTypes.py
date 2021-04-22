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

    # Many packets seem to contain position data, use generic print formatting
    # TODO: Finetune preferred formatting. Maybe drop a a couple of high/low bits
    def pos_to_string(self, pos):
        return str(pos.rjust(10)) + " "

    # Same, but with angles
    # TODO: Remember to fix
    def angle_to_string(self, angle):
        return str(angle).rjust(6) + " "

    # Same, but with movedirecton
    def movedir_to_string(self, dir):
        dir_str = ""
        if dir[0]:
            dir_str += " L" if dir[0] == 0x81 else " R"

        if dir[1]:
            dir_str += " F" if dir[0] == 0x81 else " B"

        return dir_str + " "

    # Convert packet to members
    def parse(self):
        raise NotImplementedError()

    # Print the packet to console in a formatted way
    def print(self):
        raise NotImplementedError()

    # Create a new packet based on the input
    def mod(self):
        raise NotImplementedError()

    # TODO: Evaluate further functionalities:
    # * Injection of additional packets.
    # * Method to convert the internal state of the object back into a packet --> Useful for mod(...)
