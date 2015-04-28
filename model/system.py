class OutputSystem:
    def __init__(self, output_function):
        self._output_function = output_function

    def set_level(self, level):
        self._output_function(level)


class CompoundSystem:
    def __init__(self, subsystems):
        self.subsystems = list(subsystems)

    def set_level(self, level):
        for subsystem in self.subsystems:
            subsystem.set_level(level)
