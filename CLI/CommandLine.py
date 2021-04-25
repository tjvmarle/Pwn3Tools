class Cli():
    def __init__(self):
        self.single_arg_cmd = {}
        self.multi_arg_cmd = {}
        pass

    def cmd(self, input_cmd):
        """
        Execute a given command.
            input: the entire input string given in the terminal.
        """

        if input_cmd in self.single_arg_cmd:
            self.single_arg_cmd[input_cmd]()
            return

        # Must be multi_arg_cmd, must contain at least one space-separated argument
        if " " not in input_cmd:
            print("Unknown command: [{}]".format(input_cmd))
            return

        # TODO: split on first space, find callback, execute with entire input_cmd as arg

        pass

    def set_cmd(self, cmd, callback, cmd_type):
        """
        Allow users to add new commands.
            cmd:        Input string from the terminal that should trigger this callback.
            callback:   The callback to execute. Should be func(void) for single_arg_cmd and func(string) for 
                        multi_arg_cmd.
            cmd_type:   Indicator if the cmd will be used with additional argument. Value is either 'single' or 'multi'.
            return:     True if cmd_type is valid and if there is no entry yet, False if either fails.

        """

        if cmd_type == "single" and cmd not in self.single_arg_cmd:
            self.single_arg_cmd[cmd] = callback  # should be
            return True

        if cmd_type == "multi" and cmd not in self.multi_arg_cmd:
            self.multi_arg_cmd[cmd] = callback
            return True

        return False
