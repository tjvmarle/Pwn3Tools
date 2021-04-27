class CommandListener():
    def __init__(self, CLI):
        self.cli = CLI
        self.cli.add_listener(self)

    def stop_listening(self):
        self.cli.remove_listener(self)

    def cmd(self, cmd_list):
        """
        Class specific handler for command given through the CLI
            cmd_list: list from the CLI. [0] will be the command, the rest additional arguments (if any)
        """
        pass
