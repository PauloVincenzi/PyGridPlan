## Base

| Pedido | Formato | Total (s) | F1 status | F1 build+solve (s) | F1 dt | F1 obj | F1 bound | F1 gap % | F1 1ª sol (s) | F2 status | F2 (s) | F2 obj | F2 gap % | Nota | Travas (ordem) | Perturbado | concorrência |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| basic-program | 0 | 27.58 | FEASIBLE | 0.01+26.31 | 25.60 | 6.902 | 7.387 | 6.6 | 0.75 | OPTIMAL | 1.25 | 5.841 | 0.00 | 0.923 | sala, quarto1, cozinha | quarto2 (10.00→12.50 m²) | 0/2 |
| large-house | 0 | 36.80 | FEASIBLE | 0.01+33.37 | 20.11 | 7.415 | 8.800 | 15.7 | 1.19 | OPTIMAL | 3.41 | 6.381 | 0.00 | 0.887 | sala, suite, jantar | cozinha (12.00→15.00 m²) | 2/2 |
| one-bedroom | 0 | 0.61 | OPTIMAL | 0.01+0.35 | 0.08 | 2.400 | 2.400 | 0.0 | 0.17 | OPTIMAL | 0.25 | 1.234 | 0.00 | 0.913 | sala, quarto, cozinha | banheiro (2.40→3.00 m²) | 2/2 |
| small-lot | 1 | 15.83 | OPTIMAL | 0.02+15.75 | 13.74 | 4.521 | 4.521 | 0.0 | 0.38 | OPTIMAL | 0.06 | 3.543 | 0.00 | 0.919 | sala, quarto1, quarto2 | cozinha (3.60→4.50 m²) | 2/2 |
| three-bedroom | 0 | 38.16 | FEASIBLE | 0.02+35.26 | 27.27 | 8.204 | 8.788 | 6.6 | 0.67 | OPTIMAL | 2.86 | 7.071 | 0.00 | 0.955 | sala, suite, cozinha | quarto2 (10.00→12.50 m²) | 2/2 |

## Execuções (rep 0)

| Pedido | k | Variante | dica viável | Status | Formato | Total (s) | F1 (s) | F1 dt | F1 1ª sol (s) | F1 status | F1 gap % | F2 (s) | F2 obj | Nota | travados exatos | cômodos mudados | área perturbado antes→depois (m², retângulo) | concorrência |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| one-bedroom | 0 | fast_cold | – | ok | 0 | 0.60 | 0.45 | 0.21 | 0.08 | OPTIMAL | 0.0 | 0.14 | 1.346 | 0.925 | True | 4 | 3.40→3.60 | 2/2 |
| one-bedroom | 0 | fast_partial | OPTIMAL | ok | 0 | 0.51 | 0.36 | 0.11 | 0.09 | OPTIMAL | 0.0 | 0.15 | 1.346 | 0.925 | True | 4 | 3.40→3.60 | 2/2 |
| one-bedroom | 0 | fast_hint | OPTIMAL | ok | 0 | 0.49 | 0.27 | 0.03 | 0.12 | OPTIMAL | 0.0 | 0.21 | 1.346 | 0.925 | True | 4 | 3.40→3.60 | 2/2 |
| one-bedroom | 1 | fast_cold | – | ok | 0 | 0.16 | 0.14 | 0.02 | 0.11 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 1 | fast_partial | OPTIMAL | ok | 0 | 0.23 | 0.21 | 0.02 | 0.09 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 1 | fast_hint | OPTIMAL | ok | 0 | 0.17 | 0.15 | 0.01 | 0.06 | OPTIMAL | 0.0 | 0.02 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 2 | fast_cold | – | ok | 0 | 0.10 | 0.06 | 0.00 | 0.05 | OPTIMAL | 0.0 | 0.04 | 1.313 | 0.927 | True | 2 | 3.40→3.40 | 2/2 |
| one-bedroom | 2 | fast_partial | OPTIMAL | ok | 0 | 0.03 | 0.02 | 0.00 | 0.02 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 2 | fast_hint | OPTIMAL | ok | 0 | 0.07 | 0.06 | 0.00 | 0.03 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 3 | fast_cold | – | ok | 0 | 0.09 | 0.05 | 0.00 | 0.03 | OPTIMAL | 0.0 | 0.04 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 3 | fast_partial | OPTIMAL | ok | 0 | 0.05 | 0.03 | 0.00 | 0.01 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 3 | fast_hint | OPTIMAL | ok | 0 | 0.10 | 0.08 | 0.00 | 0.03 | OPTIMAL | 0.0 | 0.02 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 1 | cold | – | ok | 0 | 0.11 | 0.10 | 0.02 | 0.08 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 1 | hinted | OPTIMAL | ok | 0 | 0.17 | 0.14 | 0.01 | 0.07 | OPTIMAL | 0.0 | 0.02 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 2 | cold | – | ok | 0 | 0.12 | 0.09 | 0.00 | 0.07 | OPTIMAL | 0.0 | 0.02 | 1.313 | 0.927 | True | 2 | 3.40→3.40 | 2/2 |
| one-bedroom | 2 | hinted | OPTIMAL | ok | 0 | 0.08 | 0.06 | 0.00 | 0.03 | OPTIMAL | 0.0 | 0.02 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 3 | cold | – | ok | 0 | 0.03 | 0.02 | 0.00 | 0.01 | OPTIMAL | 0.0 | 0.01 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| one-bedroom | 3 | hinted | OPTIMAL | ok | 0 | 0.09 | 0.05 | 0.00 | 0.03 | OPTIMAL | 0.0 | 0.04 | 1.313 | 0.925 | True | 0 | 3.40→3.40 | 2/2 |
| small-lot | 0 | fast_cold | – | ok | 1 | 16.16 | 16.04 | 13.46 | 0.34 | OPTIMAL | 0.0 | 0.12 | 3.661 | 0.928 | True | 2 | 5.20→5.20 | 2/2 |
| small-lot | 0 | fast_partial | OPTIMAL | ok | 1 | 17.38 | 17.20 | 13.85 | 0.33 | OPTIMAL | 0.0 | 0.17 | 3.661 | 0.928 | True | 2 | 5.20→5.20 | 2/2 |
| small-lot | 0 | fast_hint | OPTIMAL | ok | 1 | 17.85 | 17.77 | 13.96 | 0.09 | OPTIMAL | 0.0 | 0.08 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 1 | fast_cold | – | ok | 1 | 12.16 | 12.12 | 6.38 | 0.23 | OPTIMAL | 0.0 | 0.03 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 1 | fast_partial | OPTIMAL | ok | 1 | 10.25 | 10.21 | 5.75 | 0.09 | OPTIMAL | 0.0 | 0.04 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 1 | fast_hint | OPTIMAL | ok | 1 | 10.43 | 10.42 | 5.63 | 0.23 | OPTIMAL | 0.0 | 0.01 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 2 | fast_cold | – | ok | 1 | 2.76 | 2.71 | 0.65 | 0.33 | OPTIMAL | 0.0 | 0.05 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 2 | fast_partial | OPTIMAL | ok | 1 | 1.93 | 1.91 | 0.63 | 0.23 | OPTIMAL | 0.0 | 0.02 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 2 | fast_hint | OPTIMAL | ok | 1 | 1.52 | 1.50 | 0.57 | 0.13 | OPTIMAL | 0.0 | 0.02 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 3 | fast_cold | – | ok | 1 | 0.30 | 0.27 | 0.01 | 0.14 | OPTIMAL | 0.0 | 0.02 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 3 | fast_partial | OPTIMAL | ok | 1 | 0.11 | 0.10 | 0.01 | 0.05 | OPTIMAL | 0.0 | 0.01 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 3 | fast_hint | OPTIMAL | ok | 1 | 0.25 | 0.24 | 0.01 | 0.10 | OPTIMAL | 0.0 | 0.01 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 1 | cold | – | ok | 1 | 11.93 | 11.90 | 6.38 | 0.36 | OPTIMAL | 0.0 | 0.03 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 1 | hinted | OPTIMAL | ok | 1 | 11.84 | 11.81 | 5.62 | 0.12 | OPTIMAL | 0.0 | 0.02 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 2 | cold | – | ok | 1 | 2.01 | 1.98 | 0.65 | 0.23 | OPTIMAL | 0.0 | 0.02 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 2 | hinted | OPTIMAL | ok | 1 | 1.47 | 1.44 | 0.57 | 0.12 | OPTIMAL | 0.0 | 0.02 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 3 | cold | – | ok | 1 | 0.18 | 0.16 | 0.01 | 0.08 | OPTIMAL | 0.0 | 0.02 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| small-lot | 3 | hinted | OPTIMAL | ok | 1 | 0.22 | 0.18 | 0.01 | 0.07 | OPTIMAL | 0.0 | 0.03 | 3.661 | 0.928 | True | 0 | 5.20→5.20 | 2/2 |
| basic-program | 0 | fast_cold | – | ok | 0 | 12.72 | 11.40 | 8.07 | 0.47 | FEASIBLE | 5.9 | 1.32 | 5.763 | 0.907 | True | 8 | 10.85→14.43 | 2/2 |
| basic-program | 0 | fast_partial | OPTIMAL | ok | 0 | 14.48 | 13.08 | 8.30 | 0.25 | FEASIBLE | 5.9 | 1.38 | 5.763 | 0.907 | True | 8 | 10.85→14.43 | 2/2 |
| basic-program | 0 | fast_hint | OPTIMAL | ok | 0 | 13.99 | 11.39 | 8.47 | 0.22 | FEASIBLE | 8.6 | 2.59 | 5.763 | 0.907 | True | 8 | 10.85→14.43 | 2/2 |
| basic-program | 1 | fast_cold | – | ok | 0 | 7.36 | 7.32 | 5.89 | 0.26 | OPTIMAL | 0.0 | 0.04 | 5.689 | 0.917 | True | 6 | 10.85→12.09 | 2/2 |
| basic-program | 1 | fast_partial | OPTIMAL | ok | 0 | 9.90 | 9.80 | 4.96 | 0.40 | OPTIMAL | 0.0 | 0.09 | 5.689 | 0.917 | True | 6 | 10.85→12.09 | 2/2 |
| basic-program | 1 | fast_hint | OPTIMAL | ok | 0 | 6.25 | 6.21 | 4.83 | 0.12 | OPTIMAL | 0.0 | 0.04 | 5.689 | 0.917 | True | 6 | 10.85→12.09 | 2/2 |
| basic-program | 2 | fast_cold | – | ok | 0 | 4.91 | 4.88 | 3.06 | 0.70 | OPTIMAL | 0.0 | 0.03 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 2/2 |
| basic-program | 2 | fast_partial | OPTIMAL | ok | 0 | 4.67 | 4.64 | 2.16 | 0.27 | OPTIMAL | 0.0 | 0.03 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 2/2 |
| basic-program | 2 | fast_hint | OPTIMAL | ok | 0 | 3.10 | 3.03 | 0.86 | 0.32 | OPTIMAL | 0.0 | 0.06 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 2/2 |
| basic-program | 3 | fast_cold | – | ok | 0 | 0.41 | 0.39 | 0.12 | 0.17 | OPTIMAL | 0.0 | 0.02 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 2/2 |
| basic-program | 3 | fast_partial | OPTIMAL | ok | 0 | 0.68 | 0.65 | 0.09 | 0.28 | OPTIMAL | 0.0 | 0.03 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 2/2 |
| basic-program | 3 | fast_hint | OPTIMAL | ok | 0 | 0.36 | 0.33 | 0.07 | 0.10 | OPTIMAL | 0.0 | 0.02 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 2/2 |
| basic-program | 1 | cold | – | ok | 0 | 6.34 | 6.31 | 5.89 | 0.22 | OPTIMAL | 0.0 | 0.02 | 5.689 | 0.917 | True | 6 | 10.85→12.09 | 2/0 |
| basic-program | 1 | hinted | OPTIMAL | ok | 0 | 3.72 | 3.70 | 4.82 | 0.12 | OPTIMAL | 0.0 | 0.02 | 5.689 | 0.917 | True | 6 | 10.85→12.09 | 0/0 |
| basic-program | 2 | cold | – | ok | 0 | 2.66 | 2.62 | 3.06 | 0.35 | OPTIMAL | 0.0 | 0.03 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 0/0 |
| basic-program | 2 | hinted | OPTIMAL | ok | 0 | 1.27 | 1.25 | 0.86 | 0.13 | OPTIMAL | 0.0 | 0.02 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 0/0 |
| basic-program | 3 | cold | – | ok | 0 | 0.44 | 0.41 | 0.12 | 0.17 | OPTIMAL | 0.0 | 0.02 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 0/0 |
| basic-program | 3 | hinted | OPTIMAL | ok | 0 | 0.31 | 0.29 | 0.07 | 0.09 | OPTIMAL | 0.0 | 0.02 | 5.770 | 0.919 | True | 0 | 10.85→10.85 | 0/0 |
| three-bedroom | 0 | fast_cold | – | ok | 0 | 8.07 | 6.93 | 8.09 | 0.39 | FEASIBLE | 10.6 | 1.13 | 7.036 | 0.951 | True | 9 | 10.88→14.04 | 0/0 |
| three-bedroom | 0 | fast_partial | OPTIMAL | ok | 0 | 9.07 | 7.56 | 8.35 | 0.21 | FEASIBLE | 6.3 | 1.51 | 7.129 | 0.952 | True | 9 | 10.88→12.24 | 0/0 |
| three-bedroom | 0 | fast_hint | OPTIMAL | ok | 0 | 9.59 | 8.04 | 8.60 | 0.19 | FEASIBLE | 6.3 | 1.54 | 7.129 | 0.952 | True | 9 | 10.88→12.24 | 0/0 |
| three-bedroom | 1 | fast_cold | – | ok | 0 | 7.37 | 6.72 | 7.17 | 0.71 | OPTIMAL | 0.0 | 0.65 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 1 | fast_partial | OPTIMAL | ok | 0 | 6.64 | 5.68 | 6.91 | 0.20 | OPTIMAL | 0.0 | 0.96 | 7.021 | 0.952 | True | 2 | 10.88→10.88 | 0/0 |
| three-bedroom | 1 | fast_hint | OPTIMAL | ok | 0 | 7.43 | 6.41 | 7.06 | 0.16 | OPTIMAL | 0.0 | 1.02 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 2 | fast_cold | – | ok | 0 | 3.45 | 3.42 | 3.87 | 0.35 | OPTIMAL | 0.0 | 0.03 | 7.021 | 0.952 | True | 2 | 10.88→10.88 | 0/0 |
| three-bedroom | 2 | fast_partial | OPTIMAL | ok | 0 | 3.46 | 3.42 | 2.90 | 0.19 | OPTIMAL | 0.0 | 0.04 | 7.021 | 0.952 | True | 4 | 10.88→10.88 | 0/0 |
| three-bedroom | 2 | fast_hint | OPTIMAL | ok | 0 | 2.07 | 2.03 | 1.83 | 0.16 | OPTIMAL | 0.0 | 0.04 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 3 | fast_cold | – | ok | 0 | 2.93 | 2.90 | 1.54 | 0.27 | OPTIMAL | 0.0 | 0.02 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 3 | fast_partial | OPTIMAL | ok | 0 | 2.93 | 2.91 | 1.60 | 0.17 | OPTIMAL | 0.0 | 0.02 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 3 | fast_hint | OPTIMAL | ok | 0 | 0.76 | 0.73 | 0.42 | 0.14 | OPTIMAL | 0.0 | 0.02 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 1 | cold | – | ok | 0 | 7.10 | 6.40 | 7.17 | 0.58 | OPTIMAL | 0.0 | 0.69 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 1 | hinted | OPTIMAL | ok | 0 | 7.30 | 6.23 | 7.05 | 0.16 | OPTIMAL | 0.0 | 1.06 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 2 | cold | – | ok | 0 | 3.52 | 3.48 | 3.87 | 0.38 | OPTIMAL | 0.0 | 0.04 | 7.021 | 0.952 | True | 2 | 10.88→10.88 | 0/0 |
| three-bedroom | 2 | hinted | OPTIMAL | ok | 0 | 2.14 | 2.11 | 1.83 | 0.15 | OPTIMAL | 0.0 | 0.03 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 3 | cold | – | ok | 0 | 2.86 | 2.84 | 1.54 | 0.29 | OPTIMAL | 0.0 | 0.02 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| three-bedroom | 3 | hinted | OPTIMAL | ok | 0 | 0.77 | 0.74 | 0.43 | 0.13 | OPTIMAL | 0.0 | 0.03 | 7.021 | 0.952 | True | 0 | 10.88→10.88 | 0/0 |
| large-house | 0 | fast_cold | – | ok | 0 | 9.90 | 8.53 | 8.09 | 1.49 | FEASIBLE | 34.3 | 1.36 | 5.163 | 0.814 | True | 12 | 10.44→15.48 | 0/0 |
| large-house | 0 | fast_partial | INFEASIBLE | ok | 0 | 10.62 | 9.17 | 8.43 | 1.53 | FEASIBLE | 15.7 | 1.45 | 6.372 | 0.906 | True | 12 | 10.44→15.39 | 0/0 |
| large-house | 0 | fast_hint | INFEASIBLE | ok | 0 | 10.54 | 9.27 | 8.43 | 1.59 | FEASIBLE | 15.7 | 1.26 | 6.372 | 0.906 | True | 12 | 10.44→15.39 | 0/0 |
| large-house | 1 | fast_cold | – | ok | 0 | 8.34 | 8.30 | 8.11 | 0.65 | FEASIBLE | 34.7 | 0.04 | 5.033 | 0.814 | True | 11 | 10.44→21.83 | 0/0 |
| large-house | 1 | fast_partial | INFEASIBLE | ok | 0 | 10.85 | 8.84 | 8.41 | 5.56 | FEASIBLE | 33.5 | 2.01 | 4.901 | 0.808 | True | 11 | 10.44→15.34 | 0/0 |
| large-house | 1 | fast_hint | INFEASIBLE | ok | 0 | 10.52 | 8.52 | 8.41 | 5.17 | FEASIBLE | 33.5 | 1.99 | 4.901 | 0.808 | True | 11 | 10.44→15.34 | 0/0 |
| large-house | 2 | fast_cold | – | ok | 0 | 7.18 | 7.14 | 7.73 | 0.94 | OPTIMAL | 0.0 | 0.03 | 6.429 | 0.883 | True | 6 | 10.44→13.05 | 0/0 |
| large-house | 2 | fast_partial | INFEASIBLE | ok | 0 | 8.80 | 8.76 | 8.26 | 2.39 | OPTIMAL | 0.0 | 0.03 | 6.429 | 0.883 | True | 4 | 10.44→13.05 | 0/0 |
| large-house | 2 | fast_hint | INFEASIBLE | ok | 0 | 8.77 | 8.73 | 8.26 | 2.35 | OPTIMAL | 0.0 | 0.04 | 6.429 | 0.883 | True | 4 | 10.44→13.05 | 0/0 |
| large-house | 3 | fast_cold | – | ok | 0 | 4.10 | 4.06 | 4.23 | 0.59 | OPTIMAL | 0.0 | 0.04 | 4.879 | 0.845 | True | 6 | 10.44→16.56 | 0/0 |
| large-house | 3 | fast_partial | INFEASIBLE | ok | 0 | 4.90 | 4.87 | 4.57 | 1.20 | OPTIMAL | 0.0 | 0.03 | 4.879 | 0.845 | True | 6 | 10.44→16.56 | 0/0 |
| large-house | 3 | fast_hint | INFEASIBLE | ok | 0 | 4.70 | 4.66 | 4.57 | 1.15 | OPTIMAL | 0.0 | 0.03 | 4.879 | 0.845 | True | 6 | 10.44→16.56 | 0/0 |
| large-house | 1 | cold | – | ok | 0 | 26.60 | 25.92 | 25.34 | 0.62 | FEASIBLE | 26.6 | 0.67 | 5.605 | 0.849 | True | 11 | 10.44→21.83 | 0/0 |
| large-house | 1 | hinted | INFEASIBLE | ok | 0 | 27.24 | 26.67 | 25.47 | 5.47 | FEASIBLE | 17.9 | 0.56 | 6.271 | 0.886 | True | 11 | 10.44→13.50 | 0/0 |
| large-house | 2 | cold | – | ok | 0 | 7.14 | 7.10 | 7.73 | 1.01 | OPTIMAL | 0.0 | 0.04 | 6.429 | 0.883 | True | 6 | 10.44→13.05 | 0/0 |
| large-house | 2 | hinted | INFEASIBLE | ok | 0 | 9.11 | 9.07 | 8.52 | 2.52 | OPTIMAL | 0.0 | 0.03 | 6.429 | 0.883 | True | 4 | 10.44→13.05 | 0/0 |
| large-house | 3 | cold | – | ok | 0 | 4.04 | 4.01 | 4.23 | 0.60 | OPTIMAL | 0.0 | 0.03 | 4.879 | 0.845 | True | 6 | 10.44→16.56 | 0/0 |
| large-house | 3 | hinted | INFEASIBLE | ok | 0 | 4.67 | 4.62 | 4.57 | 1.05 | OPTIMAL | 0.0 | 0.04 | 4.879 | 0.845 | True | 6 | 10.44→16.56 | 0/0 |
| one-bedroom | 0 | cold | – | ok | 0 | 0.68 | 0.53 | 0.21 | 0.14 | OPTIMAL | 0.0 | 0.15 | 1.346 | 0.925 | True | 4 | 3.40→3.60 | 0/0 |
| one-bedroom | 0 | hinted | OPTIMAL | ok | 0 | 0.26 | 0.15 | 0.03 | 0.04 | OPTIMAL | 0.0 | 0.10 | 1.346 | 0.925 | True | 4 | 3.40→3.60 | 0/0 |
