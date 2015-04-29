class OutputSystem:
    """A system which sends its level out on an output address"""

    def __init__(self, address, output):
        self._address = address
        self._output = output

    def set_level(self, level):
        self._output.set_level(self._address, level)


class CompoundSystem:
    """A system made up of one or more subsystems"""

    def __init__(self, subsystems):
        self.subsystems = list(subsystems)

    def set_level(self, level):
        for subsystem in self.subsystems:
            subsystem.set_level(level)
