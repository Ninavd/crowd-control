import matplotlib.pyplot as plt 
import numpy as np 
from numpy import ndarray
import random 

from classes.lattice import Lattice
from classes.cell import Cell

get_value_array = np.vectorize(lambda cell: cell.value)

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
        self.populate_corridor()
        self.populated_cells : ndarray[Cell] = self.corridor.get_populated_cells()
    
    def populate_corridor(self):
        """
        Randomly assign equal parts left-moving and right-moving to the lattice.
        """
        assert self.N <= self.corridor.cells.size, 'Number of people is larger than number of cells'
        
        for _ in range(self.N):
            value = 1 if random.random() < 0.5 else -1
            self.populate_random_cell(value)

    def populate_cell(self, cell, value):
        '''
        Populate cell with a left or right-moving individual if it is empty.
        '''
        assert isinstance(value, int) and value in [-1, 1]

        if not cell.is_empty():
            return False
        
        cell.populate(value)
        return True
    
    def populate_random_cell(self, value):
        """
        Populate a random cell and return its position
        """
        cell = self.corridor.get_random_cell()
        while not self.populate_cell(cell, value):
            cell = self.corridor.get_random_cell()
        return cell

    def iteration(self):
        """
        Execute one timestep of the CA.
        """
        # decide next cell for all populated cells 
        next_cells = []
        for cell in self.populated_cells:
            
            if cell.y == 0 and cell.value == -1:
                # random EMPTY edge cell with y=len_y - 1
                best_neighbor = self.corridor.get_random_empty_edge_cell(y=self.corridor.len_y - 1, x = cell.x)
            elif cell.y == self.corridor.len_y - 1 and cell.value == 1:
                # random EMPTY edge cell with y=0
                best_neighbor = self.corridor.get_random_empty_edge_cell(y=0, x=cell.x)
            else:
                best_neighbor = cell.get_best_neighbor()
                
            # TODO: If two neighbors have same distance, pick a random one
            # TODO: If two cells want to move to the same cell, choose randomly which one gets to move.
            if best_neighbor and best_neighbor not in next_cells:
                next_cells.append(best_neighbor)
            else:
                next_cells.append(cell)

        # populate new cells and empty old ones.
        for old_cell, new_cell in zip(self.populated_cells, next_cells):
            value = old_cell.value
            old_cell.clear()
            new_cell.populate(value)

        # update populated cells
        self.populated_cells = self.corridor.get_populated_cells()

    def run(self, animate=True):
        """
        Execute self.iters amount of timesteps.
        Animate progress if animate is True.
        """
        if animate:
            plt.figure()
            plt.ion()

        for _ in range(self.iters):
            # update all cells
            self.iteration()

            if animate:
                plt.clf() 
                self.plot_snapshot()
                plt.pause(0.005)

        plt.ioff() if animate else None

    def plot_snapshot(self):
        plt.imshow(get_value_array(self.corridor.cells), interpolation="nearest", origin="upper")
        plt.colorbar()
        plt.show()