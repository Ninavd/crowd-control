import numpy as np
from matplotlib import pyplot as plt 
import numpy as np 
import matplotlib.animation as animation
import scipy.stats as stats

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

def final_phi_value(runs, p_values, rho_values, iterations, L):
    mean = np.zeros((len(p_values), len(rho_values), len(runs), iterations))
    CI_int = np.zeros((len(p_values), len(rho_values), len(runs), iterations, 2))
    significance = np.zeros((len(p_values), len(rho_values), len(runs), iterations))
    phi_value_act = np.zeros((len(p_values), len(rho_values), len(runs)))

    for p_ix, p_value in enumerate(p_values):
        for rho_ix, rho_value in enumerate(rho_values):
            for run in runs:
                counter1 = np.zeros(iterations)
                phi_values = np.genfromtxt(f'./results/raw_data/run_{int(run)}_p_{p_value}_rho_{rho_value}_L_{L}_iters_{iterations}.csv', delimiter = ',', skip_header=1)
                phi_values = phi_values[:,1]
                phi_values = phi_values
                for i in range(iterations):
                    if i > 1000 and i < 4000:
                        slope, intercept, r_value, significance[p_ix, rho_ix, int(run), i], se = stats.linregress(list([np.linspace(0, 1999, 2000), phi_values[i-1000:i+1000]]))
                        mean[p_ix, rho_ix, int(run), i] = np.mean(phi_values[i-1000:i+1000])
                        CI_int[p_ix, rho_ix, int(run), i] = np.percentile(phi_values[i-1000:i+1000], [1, 100])
            
                for i in range(iterations):
                    if i > 1000 and i < 4000:
                        # If the slope is not distinguishable from 0

                        if significance[p_ix, rho_ix, int(run), i] > 0.05:
                            counter0 = 0
                            # Count number of outliers seen by iteration i
                            for j in range(2000):
                                if phi_values[i+j-999] < CI_int[p_ix, rho_ix, int(run), i, 0]:
                                    counter0 += 1
                            counter1[i] = counter0
                        else:
                            counter1[i] = 9999
                    else:
                        counter1[i] = 9999
            
                # Find the last index that saw the least amount of outliers
                counter1_inv = counter1[::-1]
                min_value_teller = np.min(counter1_inv)
                index_min_val = list(counter1_inv).index(min_value_teller)
                actual_index = iterations - index_min_val - 1

                if counter1[actual_index] == 9999:
                    print(f'Error: for p = {p_value}, rho = {rho_value}, run = {run}, there is no steady state measured. \n \
                        We should probably lower the range of intervals we include in the linear regression \n \
                        or make the lower percentile boundary higher')

                # Save the phi_value that respresents a point in our 3D plot.
                phi_value_act[p_ix, rho_ix, int(run)] = mean[p_ix, rho_ix, int(run), actual_index]

    return phi_value_act
