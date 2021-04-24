class Packet():
    """ Abstract base class to parse the game packets. """

    def __init__(self, data):
        self.data = data      # Recieved packet
        self.new_data = None  # Placeholder for modified packets
        self.modified = False
        self.parse()

    def reverse_endian(self, byte_string):
        """
        Reverse Endianness of the string
            byte_string: string with even number of hex characters
            return:      endian-inverted string
        """

        # There's probably a more 'pythonic' way to do this
        rev_string = ""
        while len(byte_string) > 0:
            rev_string += byte_string[-2:]
            byte_string = byte_string[:-2]

        return rev_string

    # TODO: Finetune preferred formatting. Maybe drop a a couple of high/low bits
    def __pos_to_string(self, xyz):
        """
        Generic way to write out position data
            xyx:    raw_bytes, containing x, y, and z position consecutively
            return: string with space-seperated x-y-z-positions
        """
        return " ".join(str(pos).rjust(10) for pos in xyz) + " "

    # TODO: Change to degrees
    def __angles_to_string(self, angles):
        """
        Generic way to write out angle data
            angles: raw_bytes, containing theta and phi angle consecutively
            return: string with space-seperated theta-phi-angle
        """
        return " ".join(str(ang).rjust(6) for ang in angles) + " "

    def __movedir_to_string(self, md):
        """
        Generic way to write the direction the player is moving
            md:     raw_bytes, containing left/right and forward/backward direction consecutively
            return: string with space-seperated movedirections
        """
        return {0x00: "  ", 0x81: "◄ ", 0x7f: "► "}[md[0]] + \
            {0x00: "  ", 0x81: "▲ ", 0x7f: "▼ "}[md[1]]

    def parse(self):
        """Parse self.data into more meaningful members"""
        raise NotImplementedError()

    def print(self):
        """Print out member-data into a packet-specific way"""
        raise NotImplementedError()

    def __mod_packet(self):
        """Modify the received packet before resending"""
        raise NotImplementedError()

    def mod(self):
        """Public interface to trigger the creation of a new packet based on the received one"""
        self.modified = True
        self.__mod_packet()

    # TODO: Injecting addional packets should not be dependant/triggered on actually receiving one first. This should
    # probably be moved to a different class and be handled inside the PacketManager. Packets could, however, be
    # dependant on current game state/data, so there should probably some way to have the injector stay up-to-date
    def inject(self):
        """Create additional packets to send out"""
        raise NotImplementedError()

    # TODO: Evaluate further functionalities:
    # * Method to convert the internal state of the object back into a packet --> Useful for print() + mod(), since it's
    #   easier to fiddle with real values instead of raw bytes
