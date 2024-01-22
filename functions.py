import numpy as np

def pop_init(len_x, len_y, n_pop, n_exits):
    '''
    Initializing the population into a (len_x, len_y) honeycomb grid 
    with n_pop grid-spaces filled and 
    n_exits the number of exits in the hall/corridor
    '''
    pop = np.zeros((len_x, len_y))
    coordinate = np.zeros((2))
    while np.count_nonzero(pop) < n_pop:
        coordinate[0] = np.random.randint(len_x, dtype=int)
        coordinate[1] = np.random.randint(len_y, dtype=int)
        pop[int(coordinate[0]), int(coordinate[1])] = np.random.randint(1, high=n_exits+1, dtype=int)
    return pop
