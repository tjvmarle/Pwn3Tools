from Packets.PacketTypes import Position as Pos
from Packets.PacketTypes import TogglePuzzle as Tog
from importlib import reload


def get_config(client):
    """
    Seperate module to configure what can and cannot be parsed by the PacketManager
        client: indicator if the PM serves a GameHandler (GH) or ServerHandler (SH)
    """

    reload(Pos)
    reload(Tog)
    if client == "GH":
        return {
            0x6d76: Pos.Position,
            0x3031: Tog.TogglePuzzle,
            # 0x0000, : "heartbeat",
            # 0x6a70, : "jump",
            # 0x2a69, : "shoot", #inc. spells
            # 0x733d, : "wpn_switch",
        }
    else:
        return {
            # 0x6d61: "mana"
        }
