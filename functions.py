import numpy as np

def pop_init(len_x, len_y, n_pop):
    '''Initializing the population'''
    pop = np.zeros((len_x, len_y))
    coordinate = np.zeros((2))
    while sum(sum(pop)) < n_pop:
        coordinate[0] = np.random.randint(len_x, dtype=int)
        coordinate[1] = np.random.randint(len_y, dtype=int)
        pop[int(coordinate[0]), int(coordinate[1])] = 1
    return pop
