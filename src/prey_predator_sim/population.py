from dataclasses import dataclass
import matplotlib.pyplot as plt

from species import Creature, Prey, Predator


@dataclass
class HistoryElement:
    prey: int
    predators: int


class Population:

    def __init__(self, population_data, parameters):
        self._instances = set()

        for species, number in population_data.items():
            for _ in range(number):
                creature = species(**parameters[species])
                self._instances.add(creature)

        self.history = [self.n]

    def hunting(self):

        predators = [c for c in self._instances if isinstance(c, Predator) and c.alive]

        preys = [c for c in self._instances if isinstance(c, Prey) and c.alive]

        for predator, prey in zip(predators, preys):
            predator.hunt(prey)


    def natural_selection(self):

        newborns = set()

        for creature in self._instances:
            if creature.alive:
                child = creature.reproduce()

                if child is not None:
                    newborns.add(child)

        self.hunting()

        for creature in self._instances:
            if creature.alive:
                creature.kill()

        self.history.append(self.n)

        self._instances = set([creature for creature in self._instances if creature.alive])

        self._instances.update(newborns)

    def plot_history(self):
        plt.plot([h.prey for h in self.history], label="Prey")
        plt.plot([h.predators for h in self.history], label="Predators")
        plt.xlabel("n")
        plt.ylabel("Population size")
        plt.title("Population history")
        plt.legend()
        plt.show()


    @property
    def n(self):

        prey = sum(1 for c in self._instances if isinstance(c, Prey) and c.alive)
        predators = sum(1 for c in self._instances if isinstance(c, Predator) and c.alive)

        return HistoryElement(prey, predators)
