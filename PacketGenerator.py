class Generator():
    """class to generate additional packets and send to server/client"""

    def __init__(self):
        self.latest_packet = {}  # header : data (entire packet)
        pass

    def inject(self, packet_type):
        """
        Generates a list of packets based on the requested header.
            packet_type: the header of the requested packet(s)
        """
        # Generate packets
        return ()

    def update(self, data):
        """
        Keeps track of latest packet data. Forms the basis for generating new packets.
            data: a received packet
        """

        self.latest_packet[int.from_bytes(data[:2], "big")] = data
