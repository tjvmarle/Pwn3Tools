from Proxies.PwnProxy import PwnProxy
from CLI.CommandLineInput import CommandLineInput

# Run main
CLI = CommandLineInput()

SERVER_ADDRESS = "192.168.138.130"  # Set to IP of Ubuntu VM
master_port = 3333
master_server = PwnProxy(master_port, SERVER_ADDRESS, CLI)
master_server.start()

game_servers = []
for port in range(3000,3006):
    gs = PwnProxy(port, SERVER_ADDRESS, CLI)
    gs.start()
    game_servers.append(gs)

#TODO: Test runs
#TODO: Input loop