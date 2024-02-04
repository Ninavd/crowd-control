import copy
import matplotlib.pyplot as plt 
import numpy as np 
import random 

from numpy import ndarray
from collections import defaultdict
from classes.lattice import Lattice
from classes.cell import Cell
from helpers import get_value_array


class Simulation:

    """
    Simulates heterogenous crowd in an infinite corridor.

    Attributes:
        N (int): Total number of people in the corridor.
        iters (int): Number of iterations (timesteps) to execute.
        corridor (Lattice): Object representing the initial state of populated corridor.
        populated_cells (ndarray[Cell]): Array of currently populated cell objects .
        p (float): probability of agents moving straight (soberness).
    """

    def __init__(self, iters, corridor, p=1):
        """
        Initializes the simulation object.

        Args:
            N (int): Total number of people in the corridor.
            iters (int): Number of iterations (timesteps) to exectue
            corridor (Lattice): Object representing the initial state of populated corridor.
            p (float): probability of agents moving straight (soberness).
        """
        self.N = len(corridor.get_populated_cells())
        self.iters = iters
        self.corridor: Lattice = copy.deepcopy(corridor)
        self.corridor.load_neighbours()
        self.populated_cells: ndarray[Cell] = self.corridor.get_populated_cells()
        self.p = p

    def find_target_cell(self, cell: Cell) -> Cell | None:
        """
        Find and return target cell while considering boundary conditions.
        Implicitly returns None if no target cell available.

        Args:
            cell (Cell): Populated cell that needs to target next cell.
        """
        assert cell.value != 0, 'Unpopulated cell should not target a cell'

        # check periodic boundary conditions
        if cell.is_leaving_left():
            new_y = self.corridor.len_y - 1
            return self.corridor.get_random_empty_edge_cell(new_y, x=cell.x, p=self.p)
        elif cell.is_leaving_right(self.corridor.len_y):
            return self.corridor.get_random_empty_edge_cell(y=0, x=cell.x, p=self.p)
        
        # cell is not a boundary cell
        return cell.get_best_neighbor(self.p)

    def resolve_conflicts(self, next_cells):
        """
        Resolve conflicts in the next_cells dictionary.
        If cell targeted by multiple cells, random cell wins and others stay put.
        Return dict with coordinate of target cell as key, cell object as value.

        Args:
            next_cells: dict with coordinate of target cell as keys, list of cells as values.
        """
        targets = list(next_cells.keys())
        cell_assigned = {}

        for target in targets:
            candidates = next_cells[target]

            if len(candidates) == 1:
                cell_assigned[target] = candidates[0]
            else:
                for _ in range(len(candidates) - 1):
                    loser = candidates.pop(random.randint(0, len(candidates) - 1))
                    cell_assigned[(loser.x, loser.y)] = loser
                winner = candidates[0]
                cell_assigned[target] = winner
        
        return cell_assigned
    
    def execute_timestep(self, next_cells):
        """
        Populate new cells and empty old ones.
        Adjust distance value of visited cells. 

        Args:
            next_cells (dict): Defines all moves to execute.
        """
        for new_cell_coords, old_cell in next_cells.items():
            value = old_cell.value
            new_cell = self.corridor.cells[new_cell_coords]
            
            if old_cell != new_cell: 
                old_cell.lower_distance_to_exit()
            
            old_cell.clear()    
            new_cell.populate(value)

    def iteration(self):
        """
        Execute one iteration of the Cellular Automata.
        """
        # key=tuple with coords of a targeted cell, value=list of old_cell(s)
        next_cells = defaultdict(list) 
 
        for cell in self.populated_cells:
            
            target_cell = self.find_target_cell(cell)
            
            # save targeted cells
            if target_cell: 
                next_cells[(target_cell.x, target_cell.y)].append(cell)
            else:
                next_cells[((cell.x, cell.y))] = [cell] 
        
        # solve conflicts when cell is targeted by multiple cells
        next_cells = self.resolve_conflicts(next_cells)

        # populate new cells and empty old ones
        self.execute_timestep(next_cells)
        
        # update populated cells
        self.populated_cells = self.corridor.get_populated_cells()

    def run(self, animate=True, save_video=True, print_progress=True):
        """
        Execute self.iters iterations and return evolution of order parameter.

        Args:
            animate (bool): Animates progress if true.
            save_video (bool): Saves CA snapshots if true
            print_progress (bool): Prints iteration number if true.
        """
        images = []
        if animate:
            plt.figure(figsize=(12, 5))
            plt.ion()
            
        phi_0 = calculate_phi_0(self.corridor.len_x, self.corridor.len_y, self.N)
        print(f'phi_0:{phi_0:.3f}')
        phi_values = np.zeros(self.iters)
        
        for i in range(self.iters):
            print(f'iteration {i+1}/{self.iters}     ', end='\r') if print_progress else None
            
            # update all cells
            self.iteration()
            
            # update order parameter
            phi = self.corridor.calculate_lane_formation()
            phi_reduced = (phi-phi_0)/(1-phi_0)
            phi_values[i] = phi_reduced

            if save_video == True:
                images.append(get_value_array(self.corridor.cells))

            self.animate(i, phi_values) if animate else None   

        plt.ioff() if animate else None

        assert len(self.corridor.get_populated_cells()) == self.N, 'Density has changed during simulation'
        return images, phi_values
    
    def animate(self, i, phi_values):
        """
        Animates one frame of the simulation. 

        Args:
            i (int): Current iteration number.
            phi_values (list[float]): array of phi value per iteration.
        """
        # plot lattice
        plt.subplot(1,2,1)
        self.plot_snapshot(colorbar=False)

        # plot phi evolution
        plt.subplot(1,2,2)
        plt.xlabel('iteration')
        plt.ylabel('$\\tilde{\phi}$', fontsize=14)
        plt.plot(list(range(i + 1)), phi_values[0:i+1], 'k-')
        plt.pause(0.005)
        plt.clf()

    def plot_snapshot(self, colorbar=True):
        """
        Plots snapshot of the current state of the lattice.
        """
        plt.imshow(get_value_array(self.corridor.cells), interpolation="nearest", origin="upper")
        plt.colorbar() if colorbar == True else None
        plt.show()
    
    def plot_results(self, phi_values, save=False):
        """
        Plots final configuration of the lattice and progress of phi in one figure.
        """
        plt.figure(figsize=(12, 5))
        plt.subplot(121)
        plt.imshow(get_value_array(self.corridor.cells), interpolation="nearest", origin="upper")
        plt.colorbar() 

        plt.subplot(122)
        plt.xlabel('iteration')
        plt.ylabel('$\\tilde{\phi}$', fontsize=14)
        plt.plot(list(range(len(phi_values))), phi_values, 'k-')

        if save:
            density = self.N / (self.corridor.len_x * self.corridor.len_y)
            plt.savefig(f'./results/final_snapshots/L_{self.corridor.len_x}_rho_{density}_p_{self.p}.png')

def calculate_phi_0(len_x, len_y, N):
    """
    Calculates phi_0, the normalization factor for the reduced order parameter
    (measures the degree of lane formation) by generating 100 random corridors.

    Args:
        len_x (int): Number of rows of the corridor.
        len_y (int): Number of columns of the corridor.
        N (int): Number of agents in the corridor.
    """
    phi_randoms = np.zeros(100)
    for j in range(0,100):
        corridor = Lattice(len_x, len_y)
        corridor.populate_corridor(N)
        phi_randoms[j] = corridor.calculate_lane_formation()
    phi_0 = np.mean(phi_randoms)
    return phi_0
