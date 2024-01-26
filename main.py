from classes.lattice import Lattice
from classes.simulation import Simulation

x_width = 50
y_height = 50
density = 0.1
N = int(density*x_width*y_height)
iterations = 2000
Corridor = Lattice(x_width, y_height)

simulation = Simulation(N, iterations, Corridor)
print(Corridor)
# simulation.plot_snapshot()

simulation.run()