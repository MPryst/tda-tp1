import csv
import sys

alumnos_txt = open(sys.argv[1])
capitan_i = int(sys.argv[2])
alumnos_csv = csv.reader(alumnos_txt, delimiter=",")

alumnos = [row for row in alumnos_csv]
nombres = [row[0] for row in alumnos]
conocimientos = [row[1:] for row in alumnos]



