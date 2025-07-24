import csv
from lexico import analizador_lexico_cereza

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
    
    # Proceso tokens del analizador léxico
    for _, linea_tokens in resultado_lexico:
        for tok in linea_tokens:
            if tok[0].startswith("❌"):
                return f"❌ Error léxico: {tok[2]} en línea {tok[1]}"
            if tok[0] == "✅ RESERVED":
                tokens.append((tok[1], tok[1]))  # token tipo = valor, ej. ("if","if")
            elif tok[0] == "✅ IDENTIFIER":
                tokens.append(("id", tok[1]))
            elif tok[1] == "NUMBER":
                tokens.append(("number", tok[2]))
            elif tok[1] in ["LBRACE", "RBRACE", "LPAREN", "RPAREN",
                            "EQ", "NEQ", "GT", "LT",
                            "PLUS", "MINUS", "MULT", "DIV", "ASSIGN"]:
                # Se agrega con lexema igual al token para facilitar consulta
                simbolo_lexema = {
                    "LBRACE": "{", "RBRACE": "}",
                    "LPAREN": "(", "RPAREN": ")",
                    "EQ": "==", "NEQ": "!=",
                    "GT": ">", "LT": "<",
                    "PLUS": "+", "MINUS": "-",
                    "MULT": "*", "DIV": "/",
                    "ASSIGN": "="
                }
                tokens.append((simbolo_lexema[tok[1]], simbolo_lexema[tok[1]]))
                
            # Aquí manejo para 'NEWLINE'
            elif tok[0] == "NEWLINE":
                tokens.append(("NEWLINE", "\\n"))
            else:
                # Si hay token no esperado, error
                return f"❌ Error léxico: Token no reconocido '{tok}'"

    tokens.append(("$", "$"))  # EOF al final

    pila = [0]
    entrada = tokens.copy()
    # No se usará lista salida para producción ni emitir
    # solo un mensaje de éxito o falla

    while True:
        estado_actual = pila[-1]
        simbolo_actual = entrada[0][0]

        # Ignorar token NEWLINE para no interferir con tabla sin modificar
        if simbolo_actual == "NEWLINE":
            entrada.pop(0)
            continue

        print(f"⬆️ Puntero en el estado '{estado_actual}' con símbolo '{simbolo_actual}'")
        accion = tabla.get(estado_actual, {}).get(simbolo_actual)

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

            # Sacar 2 * longitud(cuerpo) elementos de la pila (símbolos y estados)
            for _ in range(2 * len(cuerpo)):
                pila.pop()
            estado_tope = pila[-1]
            pila.append(cabeza)
            nuevo_estado = tabla[estado_tope].get(cabeza)
            if nuevo_estado is None:
                return f"❌ Error: sin transición desde estado {estado_tope} con '{cabeza}'"
            pila.append(int(nuevo_estado))
        elif accion == "acc":
            return "✅ Cadena aceptada correctamente."
        else:
            return f"❌ Acción inválida '{accion}' en estado {estado_actual} con símbolo '{simbolo_actual}'"
