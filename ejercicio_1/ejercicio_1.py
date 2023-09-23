import csv
import sys

# Argumentos: Archivos habilidades y candidatos
habilidades_csv = csv.reader(open(sys.argv[1]), delimiter=",")
candidatos_csv = csv.reader(open(sys.argv[2]), delimiter=",")

# Carga de habilidades: O(N)
habilidades = []
habilidades_nombres = []
habilidades_seleccionadas = []
for fila in habilidades_csv:
    habilidades_nombres.append(fila[1])
    habilidades_seleccionadas.append(0) # 0 a N-1, correspondiente a 1  N
    habilidades.append(0)

# Carga y ordenamiento de candidatos
candidatos = []
candidatos_seleccionados = []
mejor_solucion_de_candidatos_seleccionados = []
numero_de_candidato = 1

for fila in candidatos_csv:
    candidatos_seleccionados.append(0)
    mejor_solucion_de_candidatos_seleccionados.append(0)
    candidatos.append([fila[0], list(int(x) for x in (fila[1:])), numero_de_candidato])
    numero_de_candidato += 1
candidatos.sort(key=lambda x: len(x[1]), reverse=True)

# Reasigno los numeros al tenerlos yaa ordenados por mayor cantidad de habilidades
numero_de_candidato = 1
for candidato in candidatos:
    candidato[2] = numero_de_candidato
    numero_de_candidato += 1

print("--- CANDIDATOS ---")
for c in candidatos:    
    print(c)    
print("--- HABILIDADES ---")
for h in habilidades_nombres:    
    print(h)

total_candidatos_seleccionados = 0
total_habilidades_seleccionadas = 0

mejor_total_candidatos_seleccionados = 0



# Inicio de la resolucion y definicion de funciones
def cota(nro):    
    cand_sel = total_candidatos_seleccionados
    hab = habilidades.copy()
    hab_sel = total_habilidades_seleccionadas

    for i in range(nro-1, len(candidatos)- 1):
        for h in candidatos[i][1]: # candidatos es una lista, centro de la cual hay (nombre, habilidades, numero)
            if hab[h-1] == 0: # Las habilidades van de 1 a N, pero el vector de 0 a N-1
                hab_sel += 1
                cand_sel +=1
            hab[h-1] = 1
            if hab_sel == len(habilidades)- 1:
                return cand_sel
            
    return -1

def seleccionar(num):
    candidatos_seleccionados[num-1] = 1 # el vector indexa desde 0
    total_candidatos_seleccionados +=1
    for h in candidatos[num-1][1]: # habilidades del candidato numero 'num'
        if habilidades[h-1] == 0: # Las habilidades van de 1 a N
            total_habilidades_seleccionadas +=1
        habilidades[h-1] = 1 # TODO BUG?

def deseleccionar(num):
    for h in candidatos[num-1][1]: # habilidades del candidato numero 'num'
        habilidades[h-1] -=1
        if habilidades[h-1] == 0:
            total_habilidades_seleccionadas -=1
    candidatos_seleccionados[num-1] = 0
    total_candidatos_seleccionados -=1



    
def backtrack(num):
    print("backTrack num " + str(num))
    if total_habilidades_seleccionadas == len(habilidades):
        print("total_habilidades_seleccionadas " + str(total_candidatos_seleccionados))
        if total_candidatos_seleccionados < mejor_total_candidatos_seleccionados or mejor_total_candidatos_seleccionados == 0:
            mejor_solucion_de_candidatos_seleccionados = candidatos_seleccionados.copy()
            mejor_total_candidatos_seleccionados = total_candidatos_seleccionados
            return
        else:
            return
    cota_no = cota(num)
    cota_si = cota(num+1)

    # Si ambas cotas cubren las habilidades
    if cota_no != -1 and cota_si != -1:
        # Si cotaSi es menor a cotaNo exploró esa rama primero
        if cota_si < cota_no:
            # expoloro rama de seleccionar
            seleccionar(num)
            backtrack(num + 1)
            deseleccionar(num)
            # expoloro rama de no seleccionar
            backtrack(num + 1)
        else:
            # expoloro rama de no seleccionar
            backtrack(num + 1)
            seleccionar(num)
            backtrack(num + 1)
            # expoloro rama de seleccionar
            deseleccionar(num)
    
    # Si solo cotaSi cubre todas las habilidades
    elif cota_si != -1:
        seleccionar(num)
        backtrack(num + 1)
        deseleccionar(num)
    
    # Si solo cotaNo cubre todas las habilidades
    elif cota_no != -1:
        backtrack(num + 1)




# Procesamiento del problema
numero = 1 
backtrack(numero)
if mejor_total_candidatos_seleccionados  == 0:
    print("***El problema no tiene solución***")
else:
    print("Una solución óptima del problema consta de los siguientes candidatos:")
    for i in mejor_solucion_de_candidatos_seleccionados:
        print(mejor_solucion_de_candidatos_seleccionados[i])

