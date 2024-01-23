import math 
import numpy as np
import random 

from classes.cell import Cell 
from helpers import get_neighbor_coords

get_value_array = np.vectorize(lambda cell: cell.value)

class Lattice:

    def __init__(self, len_x, len_y) -> None:
        self.len_x = len_x
        self.len_y = len_y
        self.cells = self.initialize_grid()
        self.n_cells = len_x * len_y
        self.load_neighbours()

    def initialize_grid(self):
        '''
        Load empty cell objects.
        '''
        cells = [[] for _ in range(self.len_x)]
        for x in range(self.len_x):
            for y in range(self.len_y):
                cell = Cell(
                    x,
                    y, 
                    left_exit_distance  = math.dist([self.len_x // 2, 0], [x, y]), 
                    right_exit_distance = math.dist([self.len_x // 2, self.len_y - 1], [x, y])
                    )
                cells[x].append(cell)

        cells = np.array(cells)
        return cells
    
    def load_neighbours(self):
        """
        Assign neighbors to all cell objects.
        """
        for row in self.cells:
            for cell in row:
                neighbor_coords = get_neighbor_coords(cell.x, cell.y, self.len_x, self.len_y)
                for coord in neighbor_coords:
                    neighbor = self.cells[coord]
                    cell.add_neighbor(neighbor)

    def get_random_cell(self):
        """
        Select a random cell on the lattice and return it.
        """
        random_x = random.randint(0, self.len_x - 1)
        random_y = random.randint(0, self.len_y - 1)
        return self.cells[random_x, random_y]

    def get_populated_cells(self):
        """
        Return all populated cell objects.
        """
        return self.cells[get_value_array(self.cells) != 0]

    def __str__(self) -> str:
        return f'{get_value_array(self.cells)}'