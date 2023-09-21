import csv
import sys

# Argumentos: Archivos habilidades y candidatos
habilidades_csv = csv.reader(open(sys.argv[1]), delimiter=",")
candidatos_csv = csv.reader(open(sys.argv[2]), delimiter=",")

# Habilidades[0 .. H-1] y Personas[0 .. P-1]
habilidades = []
personas = []
for fila in habilidades_csv:
    habilidades.append(fila[1])
for fila in candidatos_csv:
    personas.append([fila[0], list(int(x)-1 for x in (fila[1:]))])    

# Grupo[0 .. P-1]
grupo = len(personas) * [0]

# Variables auxiliares
grupo_auxiliar = len(personas) * [0]
habilidades_auxiliar = len(habilidades) * [0]

# Resultado final
mejor_grupo = len(personas) * [0]
max_ganancia = 0
cantidad_mejor_grupo = len(personas)


def ganancia_grupo(grupo, print_result = False):
    global habilidades_auxiliar
    habilidades_auxiliar = len(habilidades) * [0]
    
    cantidad_integrantes = 0
    # Itero las personas que esten en el grupo
    for persona_index in range(0, len(grupo)):
        if(grupo[persona_index] == 1):
            cantidad_integrantes = cantidad_integrantes + 1
            # Itero sobre sus habilidades y las voy prendiendo en el vector auxiliar
            for habilidad_index in personas[persona_index][1]:                
                habilidades_auxiliar[habilidad_index] = 1
    
    cantidad_habilidades = 0
    for i in range(0, len(habilidades_auxiliar)):
        if (habilidades_auxiliar[i] == 1):
            cantidad_habilidades = cantidad_habilidades + 1
    if print_result:
        print()
        print("\tGrupo: ", end='\t|')
        print(*grupo, sep = " | ", end='\t|')
        print("\tcantidad("+str(cantidad_integrantes)+"/"+ str(len(grupo))+")")
        print("\tHab. ", end='\t|')
        print(*habilidades_auxiliar, sep = " | ", end='|')
        print("\tcantidad("+str(cantidad_habilidades)+"/"+ str(len(habilidades))+")")
    return cantidad_habilidades   

def es_valido(grupo):    
    # Busco el ultimo (el primero en aparecer desde la derecha)
    ultima_persona_index = len(grupo)-1
    for persona_index in reversed(range(0,len(grupo))):
        if grupo[persona_index] == 1:
            ultima_persona_index = persona_index
            break
        else:
            ultima_persona_index = persona_index
    
    print("Ultimo: " + str(ultima_persona_index), end=' +: ')
    global grupo_pivote
    grupo_pivote = grupo.copy()
    for i in range(ultima_persona_index, len(grupo)):
        print(str(i), end=', ')
        grupo_pivote[i] = 1
    
    max_ganancia_pivote = ganancia_grupo(grupo_pivote)
    print()
    
    return max_ganancia_pivote == len(habilidades)


def backtrack(grupo):
    print("***Grupo*** -\t|", end='')
    print(*grupo, sep = " | ")
    ganancia_grupo_actual = ganancia_grupo(grupo, True)
    global max_ganancia
    global mejor_grupo
    global cantidad_mejor_grupo 

    cantidad_grupo_actual = 0    
    cantidad_mejor_grupo = 0
    max_ganancia = ganancia_grupo(mejor_grupo)

    for i in range(0, len(grupo)):
        if grupo[i] == 1:
            cantidad_grupo_actual = cantidad_grupo_actual + 1
        if mejor_grupo[i] == 1:
            cantidad_mejor_grupo = cantidad_mejor_grupo + 1
    
    # Si mejora, lo actualizo
    if ganancia_grupo_actual > max_ganancia or (ganancia_grupo_actual == max_ganancia and cantidad_mejor_grupo > cantidad_grupo_actual):
        print("MEJORA RESPECTO DE: ")
        ganancia_grupo(mejor_grupo, True)        
        max_ganancia = ganancia_grupo_actual
        mejor_grupo = grupo.copy()        
    
    # Funcion de corte
    if es_valido(grupo):
        # Busco el ultimo (el primero en aparecer desde la derecha)
        last_person_index = len(grupo)-1
        for person_index in reversed(range(0,len(grupo))):
            if grupo[person_index] == 1:
                last_person_index = person_index
                break
            else:
                last_person_index = person_index        
        
        print("GRUPO ANTES DE")
        print(*grupo, sep = " - ")
        for nueva_persona in range(last_person_index+1, len(grupo)):
            grupo[nueva_persona] = 1
            # Si pasa la funcion limite, sigo. Es decir, solo la agrego si mejora en algo
            if ganancia_grupo(grupo) >= ganancia_grupo_actual:
                print("Mejora al agregar: "+ str(ganancia_grupo_actual) + " -> " + str(ganancia_grupo(grupo)))
                backtrack(grupo)
            grupo[nueva_persona] = 0

backtrack(grupo)
print()
print("MEJOR GRUPO:")    
print(*mejor_grupo, sep = " | ")
for i in range(0, len(mejor_grupo)):
    if mejor_grupo[i] == 1:
        print(personas[i][0],end=', ')
print()
print('**************************************************************************************************************************')
if (max_ganancia == len(habilidades)):
    print("RESULTADO: La solucion encontrada cumple con las condiciones del problema. ¡Se cubren todas las habilidades!")
else:
    print("RESULTADO: No existe un grupo posible para cubrir todas las habilidades con los candidatos disponibles.")
print('**************************************************************************************************************************')