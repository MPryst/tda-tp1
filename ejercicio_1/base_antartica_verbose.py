import csv
import sys
import string

# Argumentos: Archivos habilidades y candidatos
try:
    habilidades_csv = csv.reader(open(sys.argv[1]), delimiter=",")
    candidatos_csv = csv.reader(open(sys.argv[2]), delimiter=",")
except:
    print("Error al leer archivos de entrada")
    exit(code=1)

# Habilidades[0 .. H-1] y Personas[0 .. P-1]
habilidades = {}
personas = []
numero_fila = 0
try:    
    for fila in habilidades_csv:
        if fila[0].isnumeric() == False:
            print(fila[0] + " no es un codigo valido para una habilidad.") 
            raise Exception("Codigo de habilidad invalido")
        habilidades[fila[0]] = numero_fila        
        numero_fila = numero_fila + 1
except:
    print("Error al cargar los datos del archivo de habilidades")
    exit(code=2)

try:
    for fila in candidatos_csv:
        personas.append([fila[0], list(habilidades[x] for x in (fila[1:]))])    
except:
    print("Error al cargar los datos del archivo de candidatos")
    exit(code=2)
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
        print("\tpersonas("+str(cantidad_integrantes)+"/"+ str(len(grupo))+")")
        print("\tHab. ", end='\t|')
        print(*habilidades_auxiliar, sep = " | ", end='|')
        print("\thabilidades("+str(cantidad_habilidades)+"/"+ str(len(habilidades))+")")
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
    global grupo_auxiliar
    grupo_auxiliar = grupo.copy()
    for i in range(ultima_persona_index, len(grupo)):
        print(str(i), end=', ')
        grupo_auxiliar[i] = 1
    
    max_ganancia_pivote = ganancia_grupo(grupo_auxiliar)
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
        
        print(*grupo, sep = " - ")
        
        personas_a_explorar = []
        for nueva_persona_index in range(last_person_index+1, len(grupo)):
            grupo[nueva_persona_index] = 1
            ganancia_con_persona = ganancia_grupo(grupo)
            grupo[nueva_persona_index] = 0

            # Si pasa la funcion costo, sigo. Si no mejora, se poda/no se recorre
            if ganancia_con_persona > ganancia_grupo_actual:
                print("Hay una mejora: "+ str(ganancia_grupo_actual) + " -> " + str(ganancia_con_persona))
                personas_a_explorar.append([nueva_persona_index, ganancia_con_persona])
        
        # Ordeno por ganancia para tener un recorrido de descendientes desde el mas prometedor
        personas_a_explorar.sort(key=lambda a: a[1], reverse=True)
        print("A recorrer los mejores ", end="")
        print(*personas_a_explorar, sep = " - ")
        for persona_con_ganancia in personas_a_explorar:
            grupo[persona_con_ganancia[0]] = 1
            backtrack(grupo)
            grupo[persona_con_ganancia[0]] = 0

backtrack(grupo)

ganancia_resultado = max_ganancia
grupo_resultado = mejor_grupo.copy()
cantidad_grupo_resultado = 0
for i in range(0, len(grupo_resultado)):
    if grupo_resultado[i] == 1:
        cantidad_grupo_resultado = cantidad_grupo_resultado + 1
        

grupo = len(personas) * [0]    
grupo_auxiliar = len(personas) * [0]
habilidades_auxiliar = len(habilidades) * [0]
mejor_grupo = len(personas) * [0]
max_ganancia = 0
cantidad_mejor_grupo = len(personas)

# Bugfix: Ejecutarlo nuevamente (contemplando el primer elemento)
grupo[0]=1
backtrack(grupo)

cantidad_integrantes_ultimo_resultado = 0
for i in range(0, len(mejor_grupo)):
    if mejor_grupo[i] == 1:
        cantidad_integrantes_ultimo_resultado = cantidad_integrantes_ultimo_resultado + 1

# Si la mejor ejecucion fue la anterior, imprimirla
if ganancia_resultado == len(habilidades) and cantidad_grupo_resultado <= cantidad_integrantes_ultimo_resultado:
    for i in range(0, len(grupo_resultado)):
        if grupo_resultado[i] == 1:
            print(personas[i][0])
    exit(0)

# Si la mejor fue la ultima, imprimirla
if (max_ganancia == len(habilidades)):
    for i in range(0, len(mejor_grupo)):
        if mejor_grupo[i] == 1:
            print(personas[i][0])
    exit(0)

print("RESULTADO: No existe un grupo posible para cubrir todas las habilidades con los candidatos disponibles.")   
