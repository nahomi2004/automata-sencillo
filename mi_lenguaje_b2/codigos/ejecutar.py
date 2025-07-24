from analizador_sintactico_slr import simular_parser
from lexico import analizador_lexico_cereza

with open("../programa.txt", encoding="utf-8") as f:
    codigo = f.read()

tokens = analizador_lexico_cereza(codigo)
for linea, resultado in tokens:
    for token in resultado:
        print(f"Línea {linea}: {token}")


#resultado = simular_parser(codigo, '../csv/Tabla_SLR_-_Base2.csv')
#print(resultado)
