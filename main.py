from classes.lattice import Lattice
from classes.simulation import Simulation

Corridor = Lattice(40, 100)

simulation = Simulation(300, 1000, Corridor)
print(Corridor)
# simulation.plot_snapshot()

simulation.run()