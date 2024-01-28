import matplotlib.pyplot as plt 
import numpy as np 
from numpy import ndarray
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
    
    def iteration(self):
        """
        Execute one timestep of the CA.
        """
        # key = tuple with coords of targeted cell, value is old_cell(s)
        next_cells = {} 

        # decide next cell for all populated cells 
        for cell in self.populated_cells:
            
            # ensure periodic boundary conditions
            if cell.y == 0 and cell.value == -1:
                best_neighbor = self.corridor.get_random_empty_edge_cell(y=self.corridor.len_y - 1, x=cell.x)
            elif cell.y == self.corridor.len_y - 1 and cell.value == 1:
                best_neighbor = self.corridor.get_random_empty_edge_cell(y=0, x=cell.x)
            else:
                best_neighbor = cell.get_best_neighbor()
            
            # pair current cell to a target cell
            if best_neighbor and (best_neighbor.x, best_neighbor.y) not in next_cells: 
                next_cells[(best_neighbor.x, best_neighbor.y)] = [cell]
            elif best_neighbor:
                next_cells[(best_neighbor.x, best_neighbor.y)].append(cell)
            else:
                next_cells[((cell.x, cell.y))] = [cell] 
        
        # If multiple cells target the same cell, choose randomly which one gets to move.
        current_keys = list(next_cells.keys())
        for key in current_keys:
            candidates = next_cells[key]

            if len(candidates) == 1:
                next_cells[key] = candidates[0]
            else:
                for _ in range(len(candidates) - 2):
                    loser = candidates.pop(random.randint(0, len(candidates) - 1))
                    next_cells[(loser.x, loser.y)] = loser
                winner = candidates[0]
                next_cells[key] = winner

        # populate new cells and empty old ones.
        for new_cell_coords, old_cell in next_cells.items():
            value = old_cell.value
            new_cell = self.corridor.cells[new_cell_coords]
            if old_cell != new_cell: 
                old_cell.lower_distance_to_exit()
            old_cell.clear()    
            new_cell.populate(value)
            


        # update populated cells
        self.populated_cells = self.corridor.get_populated_cells()

    def run(self, animate=True):
        """
        Execute self.iters amount of timesteps.
        Animate progress if animate is True.
        """
        images = []
        if animate:
            plt.figure(figsize=(12, 5))
            plt.ion()
            
        # phi_0 = np.mean(phi_randoms)
        phi_0 = calculate_phi_0(self.corridor.len_x, self.corridor.len_y, self.N)
        print(phi_0)
        phi_values = np.zeros(self.iters)

        for i in range(self.iters):
            # update all cells
            self.iteration()

            if animate: 
                plt.subplot(1,2,1)
                snapshot = self.plot_snapshot()
                images.append(snapshot)
                plt.pause(0.005)

            
            phi = calculate_lane_formation(self.corridor, self.N)
            phi_reduced = (phi-phi_0)/(1-phi_0)
            phi_values[i] = phi_reduced
            
            # plt.plot(np.linspace(1,self.iters,self.iters),phi_values)
            # plt.show()
            plt.subplot(1,2,2) if animate else None
            plt.xlabel('iteration')
            plt.ylabel('$\\tilde{\phi}$', fontsize=14)
            plt.plot(list(range(i + 1)), phi_values[0:i+1], 'k-')
            plt.show()
            plt.pause(0.005)

        plt.ioff() if animate else None
        return images, phi_values
    
    def plot_snapshot(self):
        plt.imshow(get_value_array(self.corridor.cells), interpolation="nearest", origin="upper")
        plt.colorbar()
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

