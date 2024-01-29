import argparse
import numpy as np
import scipy.stats as stats
import pandas as pd

from classes.lattice import Lattice
from classes.simulation import Simulation
from helpers import build_and_save_animation


def main(density, iterations, runs, L, animate, save_video, save_results):
    
    N = int(density * L * L)
    
    corridor = Lattice(L, L)
    corridor.populate_corridor(N)

    for i in range(runs):
        simulation = Simulation(iterations, corridor)
        images, phi_values = simulation.run(animate=animate, save_video=save_video)

        if save_video:
            build_and_save_animation(images, f'rho_{density}', iterations)
        
        if save_results:
            simulation.plot_results(phi_values, save=True)
            df = pd.DataFrame({'phi':phi_values})
            output_file = f'./results/run_{i}_rho_{density}_L_{L}_iters_{iterations}.csv'
            df.to_csv(output_file)
            print(f"Results written to {output_file}")


        
if __name__ == '__main__':

    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Simulate lane formation in heterogenic crowds")

    # adding arguments
    parser.add_argument("density", help="density of the crowd on the lattice", default=0.1, type=float)
    parser.add_argument("iterations", help="number of timesteps executed per run", default=250, type=int)
    parser.add_argument("-n", "--runs", help="number of runs", default=1, type=int)
    parser.add_argument("-s", "--size", help="size of the L x L lattice", default=50, type=int)

    parser.add_argument("-v", "--animate", action="store_true", help="visualize the simulation while running")
    parser.add_argument("--save_video", action="store_true", help="save simulation visuals to mp4")
    parser.add_argument("--save_results", action="store_true", help="store all data in a csv for each simulation/run")

    # read arguments from command line
    args = parser.parse_args()

    # print error if arguments invalid, else run main with provided arguments
    if args.density > 1 or args.density < 0:
        print("Density must lie between 0 and 1.")
    else:
        main(
            args.density, args.iterations, args.runs, args.size, 
            args.animate, args.save_video, args.save_results
            )   
