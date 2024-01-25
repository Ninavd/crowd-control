def get_neighbor_coords(x, y, len_x, len_y):
    """"
    Returns list of valid neighbor coordinates in a 2D-array.

    args:
    * x, y (int, int) - element to determine neighbors for
    * len_x, len_y (int, int) - dimensions of the 2D-array

    Returns:
    * list(tuple) - list of tuples with indeces of valid neighbors
    """
    return[
            (x_pos, y_pos) for x_pos in range(x-1, x+2)
                        for y_pos in range(y-1, y+2)
                            if  (x != x_pos or y != y_pos) and
                                (0 <= x_pos < len_x) and
                                (0 <= y_pos < len_y)]
        