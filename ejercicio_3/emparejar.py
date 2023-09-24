import csv
import sys
import math

def es_menor(a, b, ref):
    return ref[a] < ref[b]

def ordenar_contar(L, ref):
    n = len(L)
    if n <= 1:
        return 0, L
    else:
        m = n // 2

        B = L[:m]
        T = L[m:]
        # print(m, B)
        # print(n-m, T)

        inv_b, B = ordenar_contar(B, ref)
        inv_t, T = ordenar_contar(T, ref)

        inv, L = merge_contar(B, T, ref)
        # print('inv:', inv, L)
        # print(inv + inv_t+ inv_b)

    return inv_b + inv_t + inv, L

def merge_contar(A, B, ref):
    na, nb = len(A), len(B)
    L = []
    inv, i, j = 0, 0, 0
    
    while i < na and j < nb:
        a, b = A[i], B[j]
        if es_menor(a, b, ref):
            L.append(a)
            i += 1
        else:
            L.append(b)
            inv += (na - i)
            j += 1

    while j < nb:
        L.append(B[j])
        j += 1
    while i < na:
        L.append(A[i])
        i += 1
    
    return inv, L


def main():
    alumnos_csv = csv.reader(open(sys.argv[1]), delimiter=",")
    capitan_i = int(sys.argv[2]) - 1

    alumnos = [row for row in alumnos_csv]
    nombres = [row[0] for row in alumnos]
    categorias = [row[1:] for row in alumnos]
    
    longitud_categorias = len(categorias[0])
    for categoria in categorias:
        if len(categoria) != longitud_categorias:
            print('Error: Cada candidato debe tener TODAS las categorias cargadas')
            exit(code=1)

    n = len(alumnos)

    if capitan_i >= len(alumnos) or capitan_i <0:
        print('Error: El numero ingresado no corresponde a una fila de alumno')
        exit(code=1)
        
    if len(alumnos) <= 1:
        print('Error: Deben haber al menos dos participantes')
        exit(code=1)

    ref = {}
    for i, c in enumerate(categorias[capitan_i]):
        ref[c] = i

    nombre = None
    comp = 0

    for i in range(0, n):
        if i != capitan_i:
            aux = ordenar_contar(categorias[i], ref)
            if aux[0] > comp:
                comp = aux[0]
                nombre = nombres[i]

    print('El participante más complementario de', nombres[capitan_i], 'es', nombre)


if __name__ == "__main__":
    main()
