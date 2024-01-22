from classes.lattice import Lattice
from classes.simulation import Simulation

Corridor = Lattice(40, 50)

simulation = Simulation(200, 100, Corridor)
print(Corridor)
simulation.plot_snapshot()

simulation.run()