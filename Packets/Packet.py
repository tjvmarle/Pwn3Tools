class Packet():
    # Base class to parse the game packets.
    # TODO: check how 'correct' python commenting looks like

    def __init__(self, data):
        self.data = data      # Recieved packet
        self.new_data = None  # Placeholder for modified packets
        self.modified = False
        self.parse()

    # Reverse Endianness of the string
    def reverse_endian(self, byte_string):
        rev_string = ""

        # There's probably a more 'pythonic' way to do this
        while len(byte_string) > 0:
            rev_string += byte_string[-2:]
            byte_string = byte_string[:-2]

        return rev_string

    # Many packets seem to contain position data formatted the same way, so use a generic print formatting
    # TODO: Finetune preferred formatting. Maybe drop a a couple of high/low bits
    def __pos_to_string(self, xyz):
        return " ".join(str(pos).rjust(10) for pos in xyz) + " "

    # Same, but with angles
    # TODO: Change to degrees
    def __angles_to_string(self, angles):
        return " ".join(str(ang).rjust(6) for ang in angles) + " "

    # Same, but with movedirecton
    def __movedir_to_string(self, md):
        return {0x00: " ", 0x81: "L", 0x7f: "R"}[md[0]] + \
            {0x00: "  ", 0x81: "F ", 0x7f: "B "}[md[1]]

    # Convert packet to members
    def parse(self):
        raise NotImplementedError()

    # Print the packet to console in a formatted way
    def print(self):
        raise NotImplementedError()

    # Private, implement in subclass
    def __mod_packet(self):
        raise NotImplementedError()

    # Create a new packet based on the input
    def mod(self):
        self.modified = True
        self.__mod_packet()

    def inject(self):
        # Implementations should maybe follow some kind of script/scenario
        raise NotImplementedError()

    # TODO: Evaluate further functionalities:
    # * Injection of additional packets.
    # * Method to convert the internal state of the object back into a packet --> Useful for print() + mod()
