import matplotlib.pyplot as plt 
import numpy as np 
import random 

from classes.lattice import Lattice
from classes.cell import Cell

get_value_array = np.vectorize(lambda cell: cell.value)

class Simulation:

    def __init__(self, N, iters, corridor):
        self.N = N
        self.iters = iters
        self.corridor : Lattice = corridor
        self.populate_corridor()
        self.populated_cells : list[Cell] = self.corridor.get_populated_cells()
    
    def populate_corridor(self):
        assert self.N <= self.corridor.cells.size, 'Number of people is larger than number of cells'
        for _ in range(self.N):
            value = 1 if random.random() < 0.5 else -1
            self.populate_random_cell(value)

    def populate_cell(self, cell, value):
        '''
        Populate cell with a left or right-moving individual if it is empty.
        '''
        assert isinstance(value, int) and value in [-1, 1]

        if cell.is_populated():
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
        # decide next cell for all populated cells 
        next_cells = []
        for cell in self.populated_cells:
            best_neighbor = cell.get_best_neighbor()
            # TODO: If two neighbors have same distance, pick a random oneals twee neighbors dezelfde value hebben, kies er random eentje
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