from model.output import Output
from model.system import OutputSystem, CompoundSystem
from ports.art_net import ArtNetPort


class Engine():
    """The core object of an LXScript engine instance. Holds all data."""

    def __init__(self):
        self.systems = {}
        self.output = Output()
        self.ports = {ArtNetPort(self.output, 1)}

    def add_system(self, name, addresses=[], names=[]):
        systems = [OutputSystem(a, self.output) for a in addresses] + [self.systems[n] for n in names]
        if len(systems) == 1:
            self.systems[name] = systems[0]
        elif len(systems) > 1:
            self.systems[name] = CompoundSystem(systems)
        else:
            raise ValueError("empty system")
