import matplotlib.pyplot as plt
import numpy as np

from classes.lattice import Lattice
from classes.simulation import Simulation
from helpers import build_and_save_animation
import scipy.stats as stats
import pandas as pd


x_width = 50
y_height = 50
density = 0.12
N = int(density*x_width*y_height)
iterations = 500
Corridor = Lattice(x_width, y_height)

simulation = Simulation(N, iterations, Corridor)
print(Corridor)

data_frames, phi_values = simulation.run(animate=False)

build_and_save_animation(data_frames, f'test_rho_{density}', iterations)


def datacsv(it,output_file):
    results = []
    all_phi = []
    for _ in range(it):
        Corridor = Lattice(x_width, y_height)
        simulation = Simulation(N, iterations, Corridor)
        _, phi_values = simulation.run(animate=True)
        all_phi.append(phi_values)

    mean_phi = np.mean(all_phi, axis = 0)
    variance_phi = np.var(all_phi, axis = 0, ddof=1)
    df_results = pd.DataFrame({'mean_phi': mean_phi, 'variance': variance_phi})
    df_results.to_csv(output_file)
    print(f"Results written to {output_file}")

it_analyze = 2
output_file = "simulation_results.csv"
datacsv(it_analyze,output_file)
        
        
