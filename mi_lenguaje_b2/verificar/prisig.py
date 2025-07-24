import re
from collections import defaultdict

def leer_gramatica(archivo):
    with open(archivo, 'r') as f:
        lineas = [linea.strip() for linea in f if linea.strip()]
    reglas = []
    for linea in lineas:
        izq, der = linea.split('->')
        izq = izq.strip()
        der = der.strip()
        reglas.append((izq, der))
    return reglas

def es_no_terminal(simbolo):
    return simbolo.startswith('<') and simbolo.endswith('>')

def obtener_simbolos(regla_der):
    # Divide la parte derecha respetando los no terminales
    partes = []
    i = 0
    n = len(regla_der)
    while i < n:
        if regla_der[i] == '<':
            j = regla_der.find('>', i)
            partes.append(regla_der[i:j+1])
            i = j + 1
        else:
            # Agrupa terminales
            terminal = ''
            while i < n and regla_der[i] != '<':
                terminal += regla_der[i]
                i += 1
            if terminal.strip():
                for t in terminal.split():
                    partes.append(t)
    return partes

def calcular_primeros(reglas):
    first = defaultdict(set)
    # Inicializar first para terminales (son ellos mismos)
    terminales = set()
    for izq, der in reglas:
        for parte in obtener_simbolos(der):
            if not es_no_terminal(parte):
                terminales.add(parte)
    for t in terminales:
        first[t] = {t}
    # Inicializar first para no terminales
    no_terminales = {izq for izq, _ in reglas}
    changed = True
    while changed:
        changed = False
        for izq, der in reglas:
            partes = obtener_simbolos(der)
            largo_inicial = len(first[izq])
            agregar_epsilon = True
            for parte in partes:
                first[izq].update(first[parte] - {'ε'})
                if 'ε' not in first[parte]:
                    agregar_epsilon = False
                    break
            if agregar_epsilon:
                first[izq].add('ε')
            if len(first[izq]) > largo_inicial:
                changed = True
    return first

def calcular_siguientes(reglas, first):
    follow = defaultdict(set)
    no_terminales = {izq for izq, _ in reglas}
    # Inicializar follow: el símbolo inicial tiene $
    simbolo_inicial = reglas[0][0]
    follow[simbolo_inicial].add('$')
    changed = True
    while changed:
        changed = False
        for izq, der in reglas:
            partes = obtener_simbolos(der)
            for i, B in enumerate(partes):
                if not es_no_terminal(B):
                    continue
                # Siguientes de B
                largo_inicial = len(follow[B])
                beta = partes[i+1:]
                for A_beta in beta:
                    follow[B].update(first[A_beta] - {'ε'})
                    if 'ε' not in first[A_beta]:
                        break
                else:
                    follow[B].update(follow[izq])
                if len(follow[B]) > largo_inicial:
                    changed = True
    return follow

def imprimir_conjuntos(conjunto, nombre):
    for nt in conjunto:
        if nt.startswith('<'):
            valores = [v for v in sorted(conjunto[nt]) if v != 'ε']
            print(f"{nombre}({nt}) -> {', '.join(valores)}")

def main():
    reglas = leer_gramatica('../gramatica.txt')
    first = calcular_primeros(reglas)
    follow = calcular_siguientes(reglas, first)

    print("--- PRIMEROS ---")
    imprimir_conjuntos(first, "first")

    print("\n--- SIGUIENTES ---")
    imprimir_conjuntos(follow, "follow")

if __name__ == "__main__":
    main()
