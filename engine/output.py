class Output():
    """A set of numbered outputs (e.g. individual DMX channels)"""

    def __init__(self):
        self._data = {}

    def set_level(self, address, level):
        self._data[address] = level

    def get_level(self, address):
        return self._data.get(address, 0)
