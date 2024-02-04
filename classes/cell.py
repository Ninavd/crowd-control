import numpy as np
import random 

from numpy import ndarray
from helpers import get_distance_array, is_empty_vectorized

class Cell:
    """
    A cell represents a square on a lattice. 
    It may be empty or populated and has a fixed position in the lattice.

    Attributes:
        value (int): Defines if cell is populated (+/- 1) or empty (0).
        x (int): Row number of the cell
        y (int): Column number of the cell
        left_exit_distance (float):  Distance to leftt side of corridor
        right_exit_distance (float): Distance to right side of corridor
        neighbors (list[Cell]): List of neighboring cells in the lattice. 
    """

    def __init__(self, x, y, left_exit_distance, right_exit_distance) -> None:
        """
        Initializes empty Cell.

        Args:
            value (int): Defines if cell is populated (+/- 1) or empty (0).
            x (int): Row number of the cell.
            y (int): Column number of the cell.
            left_exit_distance (float):  Distance to leftt side of corridor.
            right_exit_distance (float): Distance to right side of corridor.
        """
        self.value = 0
        self.left_exit_distance = left_exit_distance
        self.right_exit_distance = right_exit_distance
        self.x = x
        self.y = y
        self.neighbors: list[Cell] = []  
       
    def is_empty(self) -> bool:
        """
        Return True if cell is unpopulated, False otherwise.
        """
        return True if self.value == 0 else False

    def is_leaving_left(self):
        """
        Returns True if agent is about to leave lattice on the left.
        """
        return self.y == 0 and self.value == -1

    def is_leaving_right(self, len_y):
        """
        Returns True if agent is about to leave lattice on the right.
        """
        return self.y == len_y - 1 and self.value == 1

    def populate(self, value) -> None:
        """
        Populate a cell if it is not empty.

        Args:
            value (int): The movement direction (-1 or +1)
        """
        assert value in [-1, 1], 'value must be 1 or -1'
        assert self.value == 0, 'can not populate un-empty cell'
        
        self.value = value
    
    def clear(self) -> None:
        """
        Empty the cell.
        """
        self.value = 0
    
    def add_neighbor(self, cell) -> None:
        """
        Add neighbouring cell object.

        Args:
            cell (object): Neighboring cell to be added.
        """
        assert len(self.neighbors) < 9, 'max number of neighbors exceeded.'

        self.neighbors.append(cell)

    def get_distance_value(self, value) -> int:
        """
        Get the correct distance value based on who is asking.

        Args:
            value (int): The movement direction (-1 or +1)
        """
        assert value != 0, 'value is ambiguous, must be -1 or 1'
        return self.right_exit_distance if value > 0 else self.left_exit_distance
    
    def get_empty_neighbors(self) -> ndarray[object]:
        """
        Return empty neighbors in array.
        """
        boolean_array = is_empty_vectorized(self.neighbors)
        return np.array(self.neighbors)[boolean_array]
    
    def get_best_neighbor(self, p) -> object | None:
        """
        Return empty neighbor cell with smallest distance to the exit.
        Return None if no empty options found.

        Args:
            p (float): Probability of choosing a horizontal neighbor
        """
        assert p >= 0 and p <= 1, 'p is a probability'

        # only consider empty neighbors
        empty_neighbors = self.get_empty_neighbors()

        # every neighbor is occupied
        if len(empty_neighbors) == 0:
            return None
        
        # find distance values of all neighbors
        distances = get_distance_array(empty_neighbors, self.value)
        current_distance = self.get_distance_value(self.value)

        # if no better cells, stay where you are
        if distances.min() >= current_distance:
            return None 
        
        # only consider neighbors with smaller distance to exit
        empty_neighbors = empty_neighbors[distances < current_distance]

        if len(empty_neighbors) == 1:
            return empty_neighbors[0]

        # check for horizontal neighbors, move there with given probability
        for i, neighbor in enumerate(empty_neighbors):

            if neighbor.x == self.x:
                if random.random() < p:
                    return neighbor
                np.delete(empty_neighbors, i)
        
        # otherwise target one of remaining cells
        return np.random.choice(empty_neighbors)
    
    def lower_distance_to_exit(self):
        """
        Dynamically lower the distance to the exit.
        Only call this method when agent is leaving the cell. 
        """
        if self.value < 0:
            self.left_exit_distance -= 0.00001

        elif self.value > 0:
            self.right_exit_distance -= 0.00001
