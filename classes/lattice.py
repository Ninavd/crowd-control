import numpy as np
import random 

from numpy import ndarray
from classes.cell import Cell 
from helpers import get_neighbor_coords, get_value_array, get_distance_array

class Lattice:
    """
    A Lattice is a 2D discrete grid of cells objects, initialized with empty cells.

    Attributes:
        len_x (int): Number of rows.
        len_y (int): Number of columns.
        cells (ndarray[Cell]): 2D array of cell objects
        n_cells (int): Number of cells in the lattice
    """

    def __init__(self, len_x, len_y) -> None:
        """
        Initializes empty Lattice object.

        Args:
            len_x (int): Number of rows.
            len_y (int): Number of columns.
        """
        self.len_x = len_x
        self.len_y = len_y
        self.cells = self.initialize_grid()
        self.n_cells = len_x * len_y

    def initialize_grid(self) -> ndarray[Cell]:
        """
        Create empty cell objects and return as an 2D array.
        """
        cells = [[] for _ in range(self.len_x)]
        for x in range(self.len_x):
            for y in range(self.len_y):
                cell = Cell(x, y, y, self.len_y - y)
                cells[x].append(cell)

        return np.array(cells)
    
    def load_neighbours(self):
        """
        Assign neighbors to all cell objects.
        """
        for cell in self.cells.flatten():
            neighbor_coords = get_neighbor_coords(cell.x, cell.y, self.len_x, self.len_y)
            for coords in neighbor_coords:
                neighbor = self.cells[coords]
                cell.add_neighbor(neighbor)
    
    def get_random_cell(self) -> Cell:
        """
        Select a random cell on the lattice and return it.
        """
        random_x = random.randint(0, self.len_x - 1)
        random_y = random.randint(0, self.len_y - 1)
        return self.cells[random_x, random_y]

    def get_random_empty_edge_cell(self, y, x, p) -> Cell | None:
        """
        Return unpopulated cell on edge around same row number. 
        Return None if no empty cell found.
        Used for periodic boundary conditions.

        Args:
            y (int): Column number of edge
            x (int): Row number of cell
            p (float): Probability of moving straight.
        """
        x_list = []
        for i in range(x-1, x+2):
            x_list.append(i) if i >= 0 and i < self.len_x else None

        # try to target cell on same row
        if self.cells[x, y].is_empty() and random.random() <= p:
            return self.cells[x, y]

        # otherwise pick a random one
        random.shuffle(x_list)
        for x_n in x_list:
            if self.cells[x_n, y].is_empty():
                return self.cells[x_n, y] 

        # no empty cell was found
        return None    
        
    def get_populated_cells(self) -> ndarray[Cell]:
        """
        Return all populated cell objects.
        """
        return self.cells[get_value_array(self.cells) != 0]

    def populate_corridor(self, N):
        """
        Randomly populate lattice with left-moving and right-moving agents.

        Args:
            N (int): Number of cells to populate.
        """
        assert N <= self.cells.size, 'Number of people is larger than number of cells'
        
        for _ in range(N):
            value = 1 if random.random() < 0.5 else -1
            self.populate_random_cell(value)

    def populate_random_cell(self, value):
        """
        Populate a random cell and return it.

        Args:
            value (int): Decides if cell is populated by right-mover or left-mover.
        """
        assert isinstance(value, int) and value in [-1, 1], 'value must be +/- 1 integer'

        cell = self.get_random_cell()
        while not self.populate_cell(cell, value):
            cell = self.get_random_cell()
        return cell
    
    def populate_cell(self, cell, value):
        """
        Populate cell with a left or right-moving individual if it is empty.
        Return True if successful, else False.

        Args:
            cell (Cell): Cell to populate.
            value (int): Decides if cell is populated by right-mover or left-mover.
        """
        assert isinstance(value, int) and value in [-1, 1]

        if not cell.is_empty():
            return False
        
        cell.populate(value)
        return True
    
    def __str__(self) -> str:
        return f'{get_distance_array(self.cells, 1)}'