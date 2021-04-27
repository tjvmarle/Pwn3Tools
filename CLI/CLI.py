class CommandLineInput():
    """Class to handle the input from the terminal while the proxies are running"""

    def __init__(self):
        self.listeners = []
        self.single_arg_cmd = {}
        self.multi_arg_cmd = {}
        pass

    def cmd(self, input_cmd):
        """
        Notify listeners of an input.
            input: the entire input string given in the terminal.
        """

        for listener in self.listeners:
            listener.listen(input_cmd.split(" "))

        return

    def remove_listener(self, listener):
        """
        Removes a listener from the list
            listener: the listener to be remove. Can be any object that implements CommandListener
        """
        self.listeners.remove(listener)

    def add_listener(self, listener):
        """
        Removes a listener from the list
            listener: the listener to dd. Can be any object that implements CommandListener. Object will be notified of 
                      each command from the CLI.
        """
        if listener in self.listeners:
            self.remove_listener(listener)

        self.listeners.append(listener)
