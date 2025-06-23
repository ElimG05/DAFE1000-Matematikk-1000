import numpy as np
import sympy as sp
import sys

print("Skriv inn likningssystemet ditt:")
smp = input("Hvor mange rader trenger du?")

Totalm = []
print("Skriv inn totalmatrisen (separert med mellomrom):")
for i in range(int(spm)):
    data = list(map(float, input(f"Skriv inn rad {i + 1}: ").split()))
    if len(data) != smp + 1:
        print("Error!")
        sys.exit()

    Totalm.append(data)

Tm = np.array(Totalm)
R = sp.Matrix(Tm).rref()[0]
print(R)

A = R[:, :-1]
b = R[:, -1]
print(A)
print (b)