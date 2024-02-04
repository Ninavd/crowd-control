# Pedestrian Counterflow: Investigating Lane formation through Cellular Automata dynamics

# Description
This project is part of the Complex System Simulation course at the UvA. A 2D Cellular Automata system is used to simulate a corridor containing two crowds of people, moving in opposite ways. The goal is to investigate the emergent phenomenon of lane formation and it's dependance on several parameters. 

# Instructions 
To perform a simulation of the system, run main.py. When doing so, several arguments can be added after the 'python main.py' command to perform the simulation in different ways. 2 arguments are always required, namely the **iterations**, giving the number of timesteps executed per run, and the **density**, giving the density of the crowd in the lattice. Run the command in the following way: 'python main.py *density iterations*' The other possible arguments and their respective function are: \
- **'-n' followed by an integer**:\
The number of simulations to execute
- **'-s' followed by an integer**:\
The size of the L x L lattice that represents the corridor 
- **'-p' followed by a float**:\
The probability of moving forward when possible(soberness parameter)
- **'-v'**:\
Animate the simulation
- **'--save_video'**:\
Save the animation to mp4 file. Requires a folder named 'simulation_videos'
- **'--save_results'**:\
Stores all data in a csv for each run

# Contributors 
The following students collaborated on this project:\
Joanna Costa e Silva \
Guido Hanegraaf \
Nina van der Meulen \ 
Kevin Schaaf