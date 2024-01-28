import matplotlib.pyplot as plt 
import numpy as np 
from numpy import ndarray
from collections import defaultdict
import random 

from classes.lattice import Lattice
from classes.cell import Cell
from helpers import get_value_array


class Simulation:

    def __init__(self, N, iters, corridor):
        """
        Initializes simulation object.
        N (int)            - Total nr of people in the corridor.
        iters (int)        - number of iterations to exectue
        corridor (Lattice) - object representing the floor plan
        populated_cells (ndarray[Cell]) - array of cell objects currently populated
        """
        self.N = N
        self.iters = iters
        self.corridor : Lattice = corridor
        self.corridor.populate_corridor(N)
        self.populated_cells : ndarray[Cell] = self.corridor.get_populated_cells()
    
    def find_target_cell(self, cell: Cell) -> Cell | None:
        """
        Finds the target cell for a given cell while considering boundary conditions.
        Returns None if no target available.
        """
        # check periodic boundary conditions
        if cell.is_leaving_left():
            new_y = self.corridor.len_y - 1
            return self.corridor.get_random_empty_edge_cell(new_y, x=cell.x)
        elif cell.is_leaving_right(self.corridor.len_y):
            return self.corridor.get_random_empty_edge_cell(y=0, x=cell.x)
        
        # cell is not a boundary cell
        return cell.get_best_neighbor()

    def resolve_conflicts(self, next_cells):
        """
        Resolve conflicts in the next_cells dictionary.
        If cell targeted by multiple cells, random one wins, others stay put.
        """
        targets = list(next_cells.keys())
        cell_assigned = {}

        for target in targets:
            candidates = next_cells[target]

            if len(candidates) == 1:
                cell_assigned[target] = candidates[0]
            else:
                for _ in range(len(candidates) - 2):
                    loser = candidates.pop(random.randint(0, len(candidates) - 1))
                    cell_assigned[(loser.x, loser.y)] = loser
                    
                winner = candidates[0]
                cell_assigned[target] = winner
        
        return cell_assigned
    
    def execute_timestep(self, next_cells):
        """
        Populate new cells and empty old ones.
        Adjust distance value of visited cells.
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
        Execute one iteration of the CA.
        """
        # key = tuple with coords of targeted cell, value is old_cell(s)
        next_cells = defaultdict(list) 

        # decide next cell for all populated cells 
        for cell in self.populated_cells:
            
            target_cell = self.find_target_cell(cell)
            
            # save targeted cells
            if target_cell: 
                next_cells[(target_cell.x, target_cell.y)].append(cell)
            else:
                next_cells[((cell.x, cell.y))] = [cell] 
        
        # solve conflicts where cell is targeted by multiple cells
        next_cells = self.resolve_conflicts(next_cells)

        # populate new cells and empty old ones
        self.execute_timestep(next_cells)
        
        # update populated cells
        self.populated_cells = self.corridor.get_populated_cells()

    def run(self, animate=True, save_video=True, print_progress=True):
        """
        Execute self.iters amount of timesteps.
        Animate progress if animate is True.
        """
        images = []
        if animate:
            plt.figure(figsize=(12, 5))
            plt.ion()
            
        phi_0 = calculate_phi_0(self.corridor.len_x, self.corridor.len_y, self.N)
        print(phi_0)
        phi_values = np.zeros(self.iters)

        for i in range(self.iters):
            
            print(f'iteration {i+1}/{self.iters}     ', end='\r') if print_progress else None

            # update all cells
            self.iteration()

            phi = calculate_lane_formation(self.corridor, self.N)
            phi_reduced = (phi-phi_0)/(1-phi_0)
            phi_values[i] = phi_reduced

            if animate: 
                # plot lattice
                plt.subplot(1,2,1)
                snapshot = self.plot_snapshot(colorbar=False)
                images.append(snapshot) if save_video == True else None

                # plot phi evolution
                plt.subplot(1,2,2) if animate else None
                plt.xlabel('iteration')
                plt.ylabel('$\\tilde{\phi}$', fontsize=14)
                plt.plot(list(range(i + 1)), phi_values[0:i+1], 'k-')
                plt.pause(0.005)
                plt.clf()

        plt.ioff() if animate else None

        assert len(self.corridor.get_populated_cells()) == self.N, 'Density has changed'
        return images, phi_values
    
    def plot_snapshot(self, colorbar=True):
        plt.imshow(get_value_array(self.corridor.cells), interpolation="nearest", origin="upper")
        plt.colorbar() if colorbar == True else None
        plt.show()
        return get_value_array(self.corridor.cells)

def calculate_phi_0(len_x, len_y, N):
    phi_randoms = np.zeros(100)
    for j in range(0,100):
        corridor = Lattice(len_x, len_y)
        corridor.populate_corridor(N)
        phi_randoms[j] = calculate_lane_formation(corridor, N)
    phi_0 = np.mean(phi_randoms)
    return phi_0


def calculate_lane_formation(corridor, N):
    phi = 0
    value_array = get_value_array(corridor.cells)
    for row in range(corridor.len_x):
        counter_left = np.count_nonzero(value_array[row] == -1)
        counter_right = np.count_nonzero(value_array[row] == 1)
        if counter_left + counter_right > 0:
            phi += ((counter_left - counter_right)**2/(counter_left + counter_right))/N
    return phi

