#!/bin/bash

rho_values=(0.06 0.08)
p_values=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)

for rho in "${rho_values[@]}"
do
    for p in "${p_values[@]}"
    do
        python3 main.py $rho 2000 -n 10 -p $p --save_results
    done
done