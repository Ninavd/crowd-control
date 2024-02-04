# Pedestrian Counterflow: Investigating Lane formation through Cellular Automata dynamics

# Description
This project is part of the Complex System Simulation course at the UvA. A 2D Cellular Automata system is used to simulate a corridor containing two crowds of people, moving in opposite ways. The goal is to investigate the emergent phenomenon of lane formation and it's dependance on several parameters. 

# Instructions 
To perform a simulation of the system, run main.py. When doing so, several arguments can be added after the 'python main.py' command to perform the simulation in different ways. 2 arguments are always required, namely the **iterations**, giving the number of timesteps executed per run, and the **density**, giving the density of the crowd in the lattice. Run the command in the following way: 'python main.py *density iterations*' where *density* is a value between 0 and 1, and *iterations* is an integer. The other possible arguments are optional and their respective function are: 
- **'-n' followed by an integer**:\
The number of simulations/runs to execute(default 1)
- **'-s' followed by an integer**:\
The size of the L x L lattice that represents the corridor(default 50)
- **'-p' followed by a float between 0 and 1**:\
Soberness parameter: The probability of moving forward when possible(default 1)
- **'-v'**:\
Animate the simulation
- **'--save_video'**:\
Save the animation to mp4 file. Requires a folder named 'simulation_videos'
- **'--save_results'**:\
Stores all data in a csv for each simulation/run

# Contributors 
The following students collaborated on this project:
- Joanna Costa e Silva 
- Guido Hanegraaf
- Nina van der Meulen 
- Kevin Schaaf