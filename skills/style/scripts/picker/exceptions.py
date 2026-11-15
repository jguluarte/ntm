class NoHooks(Exception):
    def __init__(self):
        super().__init__("no pool in the options file gives a hook")
