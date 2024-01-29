#!/bin/bash

rho_values=(0.01 0.05 0.1 0.15  0.2 0.25 0.3)
for rho in "${rho_values[@]}"
do
    python3 main.py $rho 2000 -n 10 --save_results
done