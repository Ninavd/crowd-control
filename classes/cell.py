import numpy as np
import random 

get_distance_array = lambda cell, value : cell.left_exit_distance if value < 0 else cell.right_exit_distance
get_distance_array = np.vectorize(get_distance_array)

class Cell:

    def __init__(self, x, y, left_exit_distance, right_exit_distance) -> None:
        self.value = 0
        self.left_exit_distance = left_exit_distance
        self.right_exit_distance = right_exit_distance
        self.x = x
        self.y = y
        self.neighbors: list[Cell] = []  
       
    def is_empty(self):
        return True if self.value == 0 else False

    def populate(self, value):
        """
        Populate a cell if it is not empty.
        """
        assert value in [-1, 1]

        if self.value != 0:
            return False
        
        self.value = value
        return True
    
    def clear(self):
        """
        Empty the cell.
        """
        self.value = 0
    
    def add_neighbor(self, cell):
        """
        Add neighbouring cell object.
        """
        assert len(self.neighbors) < 10, 'max number of neighbors exceeded.'

        self.neighbors.append(cell)

    def get_distance_value(self, value):
        """
        Get the correct distance value based on who is asking.
        """
        return self.right_exit_distance if value > 0 else self.left_exit_distance
    
    def get_empty_neighbors(self):
        """
        Return empty neighbors in array
        """
        empty_neighbors = []
        for neighbor in self.neighbors:
            if neighbor.is_empty():
                empty_neighbors.append(neighbor)
        return np.array(empty_neighbors)
    
    def get_best_neighbor(self):
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
        
        minimum = distances.min()
        current_distance = self.get_distance_value(self.value)

      
        # TODO: Choose center cell with high probability, diagonal cells with a lower one.

        # if no better cells, stay where you are
        if minimum > current_distance:
            return None 
        
        # pick a random cell with lower distance
        options = list(np.where(distances < current_distance)[0])
            

        if len(options) == 1:
            return empty_neighbors[options[0]]

        for index in options:
            neighbor = empty_neighbors[index]

            if neighbor.x == self.x:
                
                if random.random() < 0.8:
                    return neighbor
                
                options.remove(index)
                # np.delete(empty_neighbors, index)
        
        best_index = random.choice(options)
        return empty_neighbors[best_index]
    
    
    