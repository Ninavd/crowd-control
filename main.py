from classes.lattice import Lattice
from classes.simulation import Simulation
from helpers import build_and_save_animation


x_width = 50
y_height = 50
density = 0.002
N = int(density*x_width*y_height)
iterations = 20
Corridor = Lattice(x_width, y_height)

simulation = Simulation(N, iterations, Corridor)
print(Corridor)

data_frames = simulation.run(animate=True)

build_and_save_animation(data_frames, f'test_rho_{density}', iterations)