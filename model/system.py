class OutputSystem:
    def __init__(self, output):
        self._output = output

    def set_level(self, level):
        self._output.set_level(level)


class CompoundSystem:
    def __init__(self, subsystems):
        self.subsystems = list(subsystems)

    def set_level(self, level):
        for subsystem in self.subsystems:
            subsystem.set_level(level)
