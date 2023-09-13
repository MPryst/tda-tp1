import csv
import sys
import math

def Ordenar_Contar(L, n):
    if n <= 1:
        return 0, L
    else:
        mid_b = math.floor(n / 2)
        mid_t = math.ceil(n / 2)

        B = L[:mid_b]
        T = L[mid_t:]

        inv_b, B = Ordenar_Contar(B, mid_b)
        inv_t, T = Ordenar_Contar(T, n - mid_t)

        inv, L = Merge_Contar(B, mid_b, T, n - mid_t)

    return inv_b + inv_t + inv, L

def Merge_Contar(A, n_a, B, n_b):
    L = [0 for _ in range(n_a + n_b)]
    inv, i, j = 0, 0, 0
    
    while i < n_a and j < n_b:
        a, b = A[i], B[j]
        if a < b:
            L[i + j] = a
            i += 1
        else:
            L[i + j] = b
            inv += n_a - i
            j += 1

    while j < n_b:
        L[i + j] = B[j]
        j += 1
    while i < n_a:
        L[i + j] = A[i]
        i += 1
    
    return inv, L


alumnos_txt = open(sys.argv[1])
capitan_i = int(sys.argv[2])
alumnos_csv = csv.reader(alumnos_txt, delimiter=",")

alumnos = [row for row in alumnos_csv]
nombres = [row[0] for row in alumnos]
conocimientos = [row[1:] for row in alumnos]
comp = 0

capitan = Ordenar_Contar(conocimientos[capitan_i], 8)
nombre = None

for i in range(0, 5):
    if i != capitan_i:
        aux = Ordenar_Contar(conocimientos[i], 8)
        if abs(aux[0] - capitan[0]) > comp:
            print(aux[0] - capitan[0], comp, capitan[0])
            comp = abs(aux[0] - capitan[0])
            complementario = aux
            nombre = nombres[i]

print(nombre, nombres[capitan_i])