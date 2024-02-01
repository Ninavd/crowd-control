#!/bin/bash

rho_values=(0.05 0.06 0.07 0.08)
p_values=(0.05 0.1 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.0)

for rho in "${rho_values[@]}"
do
    for p in "${p_values[@]}"
    do
        python3 main.py $rho 5000 -n 10 -p $p --save_results
    done
done