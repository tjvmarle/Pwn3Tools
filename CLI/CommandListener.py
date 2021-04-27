class CommandListener():
    """
    Small object to process user-input on a per-object basis
    """

    def __init__(self, CLI, cb):
        """
            CLI: reference to the central user-input-handler
            cb:  Callback to execute when a cmd is passed to this listener
        """
        self.cli = CLI
        self.cb = cb
        self.cli.add_listener(self)

    def stop_listening(self):
        """Removes this instance from the CLI. This prevents the last object reference from hanging there."""
        self.cli.remove_listener(self)

    def listen(self, cmd_list):
        """
        This method will be called by the CLI and will trigger the callback passed by the listening parent.
            cmd_list: list from the CLI. [0] will be the command, the rest additional arguments (if any)
        """
        self.cb(cmd_list)
