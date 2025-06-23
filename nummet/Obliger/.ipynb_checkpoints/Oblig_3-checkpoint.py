import numpy as np
import sympy as sp
import sys

print("Skriv inn likningssystemet ditt:")
request = int(input("Hvor mange rader trenger du?"))
#lag en if-statment som sier noe om at "request" må kun innholde èn verdi, ikke noe mellomrom

def matrixDefinerA(request):
    mA = []
    print("Skriv inn for A, koeffistientmatrisen (separert med mellomrom):")
    for i in range(request):
        data_A = list(map(float, input(f"Skriv inn rad {i + 1}: ").split()))
        dataArray_A = np.array(data_A)
        if len(data_A) != int(request):
            print("Error! Matrisen må være kvadratisk!")
            sys.exit()
    
        mA.append(data_A)
    matrixA = np.array(mA)
    return matrixA

def matrixDefinerB(request):
    mB = []
    print("Skriv inn for B, resultatvektoren (èn verdi hver rad):")
    for i in range(request):
        data_B = list(map(float, input(f"Skriv inn rad {i + 1}: ").split()))
        dataArray_B = np.array(data_B)
        if len(data_B) != 1:
            print("Error! B skal kun ha én verdi per rad")
            sys.exit()
        mB.append(data_B)
        
    matrixB = np.array(mB)
    return matrixB
    
def determinantCheck(matrixA):
    if (np.linalg.det(matrixA) <= 10e-32 and np.linalg.det(matrixA) >= -10e-32):
        print("Dette likningssystemet har ingen entydige løsninger:(")
        return False 
    return True
        
def rowReduction(matrixA, matrixB):
    totalMatrix = sp.Matrix.hstack(sp.Matrix(matrixA), sp.Matrix(matrixB))
    R = totalMatrix.rref()[0]
    print(R.evalf(3))

#-----------------------------------

matrix_A = matrixDefinerA(request)
matrix_B = matrixDefinerB(request)
if determinantCheck(matrix_A ):
    rowReduction(matrix_A , matrix_B )

#for å kjøre: run /Users/bruker/Documents/nummet/Obliger/Oblig_3.py