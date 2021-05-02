class BasePacket():
    """ Abstract base class to parse the game packets. """

    def __init__(self, data):
        self.data = data      # Received packet
        self.header_str = format(int.from_bytes(data[:2], "big"), "x").rjust(4, "0") + " "
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

    def _pos_to_string(self, xyz):
        """
        Generic way to write out position data
            xyx:    raw_bytes (4) converted to int, containing x, y, and z position consecutively
            return: string with space-seperated x-y-z-positions
        """
        return " ".join(str(pos)[1:-3].rjust(7) for pos in xyz) + " "

    def _angles_to_string(self, angles):
        """
        Generic way to write out angle data
            angles: raw_bytes (2) converted to int, containing theta, phi and some third angle consecutively
            return: string with space-seperated theta-phi-3rd-angle
        """
        return " ".join(str(round(ang / 65536 * 360, 1)).rjust(5) for ang in angles) + " "

    def _movedir_to_string(self, md):
        """
        Generic way to write the direction the player is moving
            md:     raw_bytes, containing left/right and forward/backward direction consecutively
            return: string with space-seperated movedirections
        """
        return {0x00: "  ", 0x81: "▼ ", 0x7f: "▲ "}[md[0]] + {0x00: "  ", 0x81: "◄ ", 0x7f: "► "}[md[1]]

    def parse(self):
        """Parse self.data into more meaningful members"""
        raise NotImplementedError()

    def print(self):
        """Print out member-data into a packet-specific way"""
        raise NotImplementedError()

    def _mod_packet(self):
        """Modify the received packet before resending"""
        raise NotImplementedError()

    def mod(self):
        """Public interface to trigger the creation of a new packet based on the received one"""
        self.modified = True
        self._mod_packet()

    # TODO: Injecting addional packets should not be dependant/triggered on actually receiving one first. This should
    # probably be moved to a different class and be handled inside the PacketManager. Packets could, however, be
    # dependant on current game state/data, so there should probably some way to have the injector stay up-to-date
    def inject(self):
        """Create additional packets to send out"""
        raise NotImplementedError()

    # TODO: Evaluate further functionalities:
    # * Method to convert the internal state of the object back into a packet --> Useful for print() + mod(), since it's
    #   easier to fiddle with real values instead of raw bytes
