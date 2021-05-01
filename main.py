import os
from Proxies.PwnProxy import PwnProxy
from CLI.CommandLineInput import CommandLineInput
from importlib import reload
import Packets.PacketManager


# Run main


def create_pms(cli):
    return {"GH": Packets.PacketManager.PacketManager("GH", cli), "SH": Packets.PacketManager.PacketManager("SH", cli)}


def reload_pms(proxy_list):
    for proxy in proxy_list:
        proxy.reset_pms()

    print("Reloaded PacketManagers")


CLI = CommandLineInput()

# The game starts with a [game<-->master_server] connection. Aftere logging in the master delegates this to a
# [game<-->game_server] connection
SERVER_ADDRESS = "192.168.138.130"  # Set to IP of Ubuntu VM
master_port = 3333
master_proxy = PwnProxy(master_port, SERVER_ADDRESS, create_pms(CLI), CLI)
master_proxy.start()

game_proxies = []
for port in range(3000, 3006):
    gp = PwnProxy(port, SERVER_ADDRESS, create_pms(CLI), CLI)
    gp.start()
    game_proxies.append(gp)

while True:
    try:
        cmd = input()

        if cmd[:4] == 'quit' or cmd[:4] == 'exit':
            os._exit(0)

        else:
            reload(Packets.PacketManager)
            reload_pms(game_proxies)
            print("Unknown command [{}]\n\n\n".format(cmd))
            pass

    except Exception as e:
        print("Error in command-loop: ", e)
