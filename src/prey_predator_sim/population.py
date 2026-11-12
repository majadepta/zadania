from dataclasses import dataclass
import matplotlib.pyplot as plt

from .species import Creature


@dataclass
class HistoryElement:
    prey: int
    predators: int

class Population:

    _instances: dict[type[Creature], int]
    history: list[int]  # list[HistoryElement]


    def __init__(self, n: int, **kwargs):

        self._instances = set(
            [Creature(**kwargs) for _ in range(n)]
        )

        self.history = [self.n]

    def natural_selection(self):

        newborns = set()

        for creature in self._instances:
            if creature.alive:
                child = creature.reproduce()

                if child is not None:
                    newborns.add(child)

        for creature in self._instances:
            creature.kill()

        self._instances = set([creature for creature in self._instances if creature.alive])

        self.history.append(self.n)

        self._instances.update(newborns)

    def plot_history(self):
        plt.plot(self.history)
        plt.xlabel("Pokolenie")
        plt.ylabel("Liczebność populacji")
        plt.title("Historia populacji")
        plt.show()

    @property
    def n(self):
        return len(self._instances)
