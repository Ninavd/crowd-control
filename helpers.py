import numpy as np
from matplotlib import pyplot as plt 
import numpy as np 
import matplotlib.animation as animation

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

get_value_array = np.vectorize(lambda cell: cell.value)

get_distance_array = lambda cell, value : cell.left_exit_distance if value < 0 else cell.right_exit_distance
get_distance_array = np.vectorize(get_distance_array)

is_empty_vectorized = lambda cell : cell.is_empty()
is_empty_vectorized = np.vectorize(is_empty_vectorized)


def build_and_save_animation(data_frames, title, iterations):
    """
    Animates list of 2D-arrays and saves to mp4.
    """
    fig = plt.figure()
    im = plt.imshow(np.random.randint(low=-1, high=2, size=(5, 5)), animated=True, interpolation="nearest", origin="upper")

    def animate(frame_number):
        im.set_data(data_frames[frame_number])
        return im,

    anim = animation.FuncAnimation(fig, animate, frames=iterations, interval=200, blit=True) 
    # fig.suptitle('Sine wave plot', fontsize=14) 

    # saving to m4 using ffmpeg writer 
    writervideo = animation.FFMpegWriter(fps=5) 
    anim.save(f'simulation_videos/{title}.mp4', writer=writervideo) 
    plt.close()