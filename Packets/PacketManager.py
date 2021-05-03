from CLI import CommandListener
from Packets.PacketTypes import Position as Pos
from Packets.PacketTypes import TogglePuzzle as Tog
import Packets.PacketConfig as PC
from importlib import reload

# 0x7073: probably enemy positions?fireball
filter = (
    0x0000,  # Heartbeat
    0x6d76,  # Position, also for enemies (?)
    0x6a70,  # GH - Jumping

    0x733d,  # SH - Switching weapons
    0x726c,  # SH - Reloading weapons
    0x2a69,  # GH - Firing weapon/spell
    0x6c61,  # SH - Gunshot firing
    0x6672,  # SH - Gun projectile destruction (?) - Triggers with AK47, not with pistol/handgun
    0x7878,  # SH - Terminating a spell projectile (?)

    0x7073,  # SH - Rats position

    0x2b2b,  # SH - Healing
    0x6d61,  # SH - Mana (recharge)

    # 0x6565,  # GH - Loot pickup
    # 0x6370,  # SH - Loot pickup response

    0x1703,  # GH - unk - shows periodically
    # 0x6d6b,  # SH - Rat spawn
    # 0x7374,  # SH - Rat spawn?
)
filter_client = (
    # "GH",
    # "SH",
)


class PacketManager():
    """Handle the packets of one side of the proxy, so each proxy should get 2 PM's."""

    def cmd(self, cmd_input):
        """
        This method will (eventually) implement all commands it should react to from the CLI
            cmd_input: list containing the CLI-command [0] and possible arguments [1:]
        """
        print("Cmd received:", cmd_input)

    def __init__(self, client, cli):
        # TODO: accept a Commandlistener, not a CLI
        """
        client: Signals if this PM handles either the game or the server (GH/SH)
        cli:    Reference to CLI to enable listening in on user input
        """

        self.cmd_listener = CommandListener(cli, self.cmd)
        self.packet = None
        self.receiver = None  # The intended receiver of the packet
        self.client = client

        reload(PC)
        self.packetConfig = PC.get_config(client)

    def __print_unknown(self, data):
        """
        Print a packet not defined in either dict
            data: raw bytes list
        """

        packet_string = ""
        alternator = False
        max = 50
        for byte in data:
            if max == 0:
                packet_string += "...."
                break
            packet_string += format(byte, "x").rjust(2, "0") + (" " if alternator else "")
            alternator = not alternator
            max -= 1

        print("unk", packet_string)

    def handle_packet(self, data):
        """
        Entry function for the proxy the let the PM process an incoming packet
            data:   TCP packet in the form of a raw bytes list
        """
        header = int.from_bytes(data[:2], "big")
        if header not in filter and self.client not in filter_client:
            if header in self.packetConfig:
                self.packet = self.packetConfig[header](data)

            print("[{}]: ".format(self.client), end="")
            if self.packet is None:
                self.__print_unknown(data)
            else:
                self.packet.print()

        # Should be set most of the time:
        # try:
        #     self.generator.update(data)
        # except AttributeError:
        #     pass

        out_packet = None
        if self.packet is not None and self.packet.modified:
            out_packet = self.packet.new_data
        else:
            out_packet = data

        return (out_packet,)

    # TODO: First implement the generator itself more before you hang it everywhere
    # def set_generator(self, generator):
    #     self.generator = generator

    # def inject(self, packet_type):
    #     for packet in self.generator.generate(packet_type):
    #         self.receiver.sendall(packet)
