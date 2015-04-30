class LevelSetting():
    def __init__(self, system, level):
        self._system = system
        self._level = level

    def apply(self):
        self._system.set_level(self._level)


class CompoundSetting():
    def __init__(self, subsettings):
        self._subsettings = subsettings

    def apply(self):
        for subsetting in self._subsettings:
            subsetting.apply()