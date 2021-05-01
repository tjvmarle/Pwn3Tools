import os
from Proxies.PwnProxy import PwnProxy
from CLI.CommandLineInput import CommandLineInput
from Packets.PacketManager import PacketManager as PM
from importlib import reload
import Packets.PacketManager

# Run main


def create_pms(cli):
    return {"GH": PM("GH", cli), "SH": PM("SH", cli)}


def reload_pms(pm_list):
    for pm in pm_list:
        pm.reset_pms()

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
            print("Unknown command [{}]".format(cmd))
            pass

    except Exception as e:
        print("Error in command-loop: ", e)
