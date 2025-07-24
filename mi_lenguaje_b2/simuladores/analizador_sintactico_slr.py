import csv
from analizador_lexico_cereza import analizador_lexico_cereza

# === 🧠 Cargador de Tabla SLR ===

def cargar_tabla_slr(path):
    tabla = {}
    with open(path, newline='', encoding='utf-8') as archivo_csv:
        lector = csv.DictReader(archivo_csv, delimiter=';')
        columnas = lector.fieldnames[1:]  # Ignorar columna Estado
        for fila in lector:
            estado = int(fila["Estado"])
            tabla[estado] = {}
            for col in columnas:
                celda = fila[col].strip()
                if celda:
                    tabla[estado][col] = celda
    return tabla

# === 🤖 Simulador SLR ===

def simular_parser(codigo, tabla_path):
    tabla = cargar_tabla_slr(tabla_path)
    tokens = []
    resultado_lexico = analizador_lexico_cereza(codigo)
    for _, linea_tokens in resultado_lexico:
        for tok in linea_tokens:
            if tok[0].startswith("❌"):
                return f"❌ Error léxico: {tok}"
            if tok[0] == "✅ RESERVED":
                tokens.append((tok[1], tok[1]))
            elif tok[0] == "✅ IDENTIFIER":
                tokens.append(("id", tok[1]))
            elif tok[1] == "NUMBER":
                tokens.append(("number", tok[2]))
            elif tok[1] in ["LBRACE", "RBRACE", "LPAREN", "RPAREN"]:
                tokens.append((tok[2], tok[2]))
            elif tok[1] == "OPERATOR":
                tokens.append((tok[2], tok[2]))
    tokens.append(("$", "$"))  # EOF

    pila = [0]
    entrada = tokens.copy()
    salida = []

    while True:
        estado_actual = pila[-1]
        simbolo_actual = entrada[0][0]

        accion = tabla.get(estado_actual, {}).get(simbolo_actual)

        if accion is None:
            return f"❌ Error sintáctico en estado {estado_actual} con símbolo '{simbolo_actual}'"

        if accion.startswith("s"):  # Shift
            nuevo_estado = int(accion[1:])
            pila.append(simbolo_actual)
            pila.append(nuevo_estado)
            entrada.pop(0)
        elif accion.startswith("r"):  # Reduce
            producciones = [
                ("P'", ["P"]),
                ("P", ["B"]),
                ("B", ["S"]),
                ("B", ["S", "B"]),
                ("S", ["D"]),
                ("S", ["I"]),
                ("S", ["W"]),
                ("D", ["var", "id", "=", "E"]),
                ("I", ["if", "(", "C", ")", "{", "B", "}"]),
                ("W", ["while", "(", "C", ")", "{", "B", "}"]),
                ("C", ["id", "==", "id"]),
                ("C", ["id", "!=", "id"]),
                ("C", ["id", ">", "id"]),
                ("C", ["id", "<", "id"]),
                ("E", ["T", "+", "E"]),
                ("E", ["T", "-", "E"]),
                ("E", ["T"]),
                ("T", ["F", "*", "T"]),
                ("T", ["F", "/", "T"]),
                ("T", ["F"]),
                ("F", ["number"]),
                ("F", ["id"]),
                ("F", ["(", "E", ")"])
            ]
            num_prod = int(accion[1:])
            cabeza, cuerpo = producciones[num_prod]
            for _ in range(2 * len(cuerpo)):
                pila.pop()
            estado_tope = pila[-1]
            pila.append(cabeza)
            nuevo_estado = tabla[estado_tope].get(cabeza)
            if nuevo_estado is None:
                return f"❌ Error: sin transición desde estado {estado_tope} con '{cabeza}'"
            pila.append(int(nuevo_estado))
            salida.append(f"{cabeza} → {' '.join(cuerpo)}")
        elif accion == "acc":
            return "✅ Cadena aceptada correctamente. Reducciones:" + " ".join(salida)
