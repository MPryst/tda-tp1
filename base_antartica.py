import csv
import sys

habilidades_txt = open(sys.argv[1])
candidatos_txt = open(sys.argv[2])
habilidades_csv = csv.reader(habilidades_txt, delimiter=",")
candidatos_csv = csv.reader(candidatos_txt, delimiter=",")
