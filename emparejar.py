import csv
import sys
import math

def es_menor(a, b, ref):
    ia, ib = 0, 0
    while ref[ia] is not a:
        ia += 1
    while ref[ib] is not b:
        ib += 1
    return ia < ib

def ordenar_contar(L, n, ref):
    if n <= 1:
        return 0, L
    else:
        mid_b = math.floor(n / 2)
        mid_t = math.ceil(n / 2)

        B = L[:mid_b]
        T = L[mid_t:]

        inv_b, B = ordenar_contar(B, mid_b, ref)
        inv_t, T = ordenar_contar(T, n - mid_t, ref)

        inv, L = merge_contar(B, mid_b, T, n - mid_t, ref)

    return inv_b + inv_t + inv, L

def merge_contar(A, n_a, B, n_b, ref):
    L = [0 for _ in range(n_a + n_b)]
    inv, i, j = 0, 0, 0
    
    while i < n_a and j < n_b:
        a, b = A[i], B[j]
        if es_menor(a, b, ref):
            L[i + j] = a
            i += 1
        else:
            L[i + j] = b
            inv += (n_a - i)
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
n = len(alumnos)
comp = 0

nombre = None
comp = 0

for i in range(0, n):
    if i != capitan_i:
        aux = ordenar_contar(conocimientos[i], 8, conocimientos[capitan_i])
        if aux[0] > comp:
            comp = aux[0]
            complementario = aux
            nombre = nombres[i]

print(nombre, nombres[capitan_i])
