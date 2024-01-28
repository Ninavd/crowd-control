import numpy as np
import random 

from numpy import ndarray
from helpers import get_distance_array, is_empty_vectorized

class Cell:

    def __init__(self, x, y, left_exit_distance, right_exit_distance) -> None:
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
        """
        assert len(self.neighbors) < 9, 'max number of neighbors exceeded.'

        self.neighbors.append(cell)

    def get_distance_value(self, value) -> int:
        """
        Get the correct distance value based on who is asking.
        """
        return self.right_exit_distance if value > 0 else self.left_exit_distance
    
    def get_empty_neighbors(self) -> ndarray[object]:
        """
        Return empty neighbors in array.
        """
        boolean_array = is_empty_vectorized(self.neighbors)
        return np.array(self.neighbors)[boolean_array]
    
    def get_best_neighbor(self) -> object | None:
        """
        Find neighbor cell with smallest distance to the relevant exit.
        Only looks at empty cells for now. 
        """
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
                
                if random.random() < 0.8:
                    return neighbor
                
                np.delete(empty_neighbors, i)
        
        # otherwise target a diagonal cell
        return np.random.choice(empty_neighbors)
    
    def lower_distance_to_exit(self):
        '''
        This function lowers the value of the distance to the exit
        In an effort to create a dynamic floorplan in which
        people prefer behind someone else because the probability
        of collisions is lower.
        '''
        if self.value < 0:
            self.left_exit_distance += -0.00001

        elif self.value > 0:
            self.right_exit_distance += -0.00001
