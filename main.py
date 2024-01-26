from classes.lattice import Lattice
from classes.simulation import Simulation
from helpers import build_and_save_animation


Corridor = Lattice(50, 50)

simulation = Simulation(200, 15, Corridor)
print(Corridor)

data_frames = simulation.run(animate=True)

build_and_save_animation(data_frames, title='test.mp4')