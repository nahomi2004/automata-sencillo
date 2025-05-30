import re

# Palabras que no se pueden usar como nombres de variables
RESERVED = {"var", "if", "else", "while", "for", "true", "false"}

# Operadores mal escritos que deben marcarse como error
BAD_OPERATORS = {'=>', '=<', '==>', '<==', '===', '!==', '->', '<-', '><'}

# Detecta si alguien escribe = = en vez de ==
SEPARATED_EQ = re.compile(r"= =")

# Define los tipos de tokens: numeros, strings, booleanos, identificadores, operadores, etc.
TOKEN_REGEX = [
    ("COMMENT_LINE", r"#.*"),
    ("STRING", r"\".*?\"|'.*?'"),
    ("NUMBER", r"-?\d+\.\d+|-?\d+"),
    ("BOOLEAN", r"\btrue\b|\bfalse\b"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SEMICOLON", r";"),
    ("COMMA", r","),
    ("OPERATOR", r"==|!=|<=|>=|&&|\|\||\+\+|--|[+\-*/%<>=&|]"),
    ("IDENTIFIER", r"[a-zA-Z][a-zA-Z0-9]*"),
    ("WS", r"\s+"),
    ("UNKNOWN", r".")
]

# Se copilan en una mega expresion regular para usarse en tokenize
TOKEN_RE = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_REGEX)
)

# Omite los espacios (WS)
# Marca como UNKNOWN a aquellas expresiones no coincidentes con nada
# Esto es lo que devuelve por ejemplos: 
# [("IDENTIFIER", "var"), ("IDENTIFIER", "x"), ("OPERATOR", "="), ("NUMBER", "5")]
def tokenize(line):
    pos = 0
    tokens = []
    while pos < len(line):
        match = TOKEN_RE.match(line, pos)
        if not match:
            tokens.append(("UNKNOWN", line[pos]))
            pos += 1
            continue
        kind = match.lastgroup
        value = match.group()
        if kind != "WS":
            tokens.append((kind, value))
        pos = match.end()
    return tokens

# Esta funcion en general valida si un identificador es correcto
# Recordar que los identificadores son los nombres de las variables
# No pueden empezar con - o _, ni tampoco ser palabras reservadas
# Si hay errores, devuelve False y un mensaje 
def is_valid_identifier(name):
    if name in RESERVED:
        # Verifica que no sea una palabra reservada
        return False, "No puede usar palabra reservada como identificador."
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", name):
        if re.match(r"^[0-9]", name):
            # Verifica que no empiece con numero
            return False, "❌ Identificador no puede comenzar con número."
        if re.match(r"^_", name):
            # Verifica que no empiece con _
            return False, "❌ Identificador no puede comenzar con guion bajo."
        if re.match(r"^-", name):
            # Verifica que no empiece con -
            return False, "❌ Identificador no puede comenzar con guion."
        if " " in name:
            # Verifica que no tenga espacios
            return False, "❌ Identificador no puede contener espacios."
        if re.search(r"[^a-zA-Z0-9]", name):
            # Verifica que contenga caracteres invalidos
            return False, "❌ Identificador contiene caracteres inválidos."
        return False, "❌ Identificador inválido."
    # Devuleve mensaje de Identificador valido
    return True, "✅ Identificador válido."

# Verifica que los elementos de una lista {} sean del mismo tipo
def check_list_homogeneity(elements):
    types = set()
    for e in elements:
        # Solo acepta int, float, boolean, string
        if re.fullmatch(r"-?\d+", e):
            types.add("int")
        elif re.fullmatch(r"-?\d+\.\d+", e):
            types.add("float")
        elif e in ("true", "false"):
            types.add("bool")
        elif re.fullmatch(r"(['\"])(?:\\.|(?!\1).)*\1", e):
            types.add("string")
        else:
            # Si hay un elemento invalido envia un mensaje
            return False, f"Elemento inválido en lista: {e}"
    return len(types) == 1, f"Lista no homogénea: contiene tipos {types}"

# Busca los bloques de comentario, si los encuentra verifica que esten 
# bien cerrados, y si lo estan los omite. En cambio si no lo estan 
# devuelve un mensaje de error
def extraer_y_marcar_comentarios_multilinea(texto):
    # Detectar comentarios multilínea no cerrados
    if texto.count("/*") != texto.count("*/"):
        print("❌ Comentario de bloque no cerrado.")
    bloques = re.findall(r"/\*.*?\*/", texto, re.DOTALL)
    texto_limpio = re.sub(r"/\*.*?\*/", "", texto, flags=re.DOTALL)
    return texto_limpio, len(bloques)

# Analiza una línea individual, ya limpia. 
def analyze_line(line, lineno):
    # Comentario de línea
    if line.strip().startswith("#"):
        print("🟡 Linea de comentario ignorada")
        return  # Ignorar línea completa

    # Advertencia por punto y coma al final
    if line.strip().endswith(";"):
        print(f"⚠️  Línea {lineno}: ';' al final de línea es ignorado.")
        line = line.rstrip(";")

    # Detectar operadores mal formados
    if SEPARATED_EQ.search(line):
        # Detecta especificamente a aquellos = = que esten separados y 
        # devuelve una advertencia 
        print(f"⚠️  Línea {lineno}: Operadores '=' separados. Use '=='.")

    for bad in BAD_OPERATORS:
        # Identifica si el operador esta invalido y envia un 
        # mensaje de error
        if bad in line:
            print(f"❌ Línea {lineno}: Operador mal formado '{bad}'.")
            return

    # Tokeniza la linea
    # Tokennizar una linea es dividir esa linea de codigo en sus 
    # partes minimas reconocibles, llamadas tokens
    tokens = tokenize(line)
    n = len(tokens)
    i = 0

    # Empieza el analisis profundo
    while i < n:
        kind, value = tokens[i]

        # Verifica si el identificador existe, si es valido
        # si despues del = haya un valor
        if kind == "IDENTIFIER" and value == "var":
            if i+1 >= n:
                print(f"❌ Línea {lineno}: Falta identificador en declaración de variable.")
                break
            id_kind, id_value = tokens[i+1]
            valid, msg = is_valid_identifier(id_value)
            
            # Devuelve un mensaje de error en caso de que valid sea False
            if not valid:
                print(f"❌ Línea {lineno}: {msg}")
                break
            if i+2 < n and tokens[i+2][1] == "=":
                if i+3 >= n:
                    print(f"❌ Línea {lineno}: Falta valor en declaración de variable.")
                    break
                val_kind, val_value = tokens[i+3]

                # Validar valor según tipo
                if val_kind == "NUMBER":
                    # No permitir espacio entre - y número
                    if val_value.startswith("-") and (i+2 < n and tokens[i+2][1] == "-" and tokens[i+3][0] == "NUMBER"):
                        print(f"❌ Línea {lineno}: Espacio entre '-' y número no permitido.")
                        break
                    
                    print("✅ Línea {lineno}: NUMBER válido.")
                    
                elif val_kind == "STRING":
                    print("✅ Línea {lineno}: STRING válido.")
                    # pass
                    
                elif val_kind == "BOOLEAN":
                    print("✅ Línea {lineno}: BOOLEAN válido.")
                    # pass
                    
                elif val_kind == "LBRACE":
                    # Analizar lista
                    elements = []
                    j = i+4
                    while j < n and tokens[j][0] != "RBRACE":
                        if tokens[j][0] in ("NUMBER", "STRING", "BOOLEAN"):
                            elements.append(tokens[j][1])
                        elif tokens[j][0] == "COMMA":
                            pass
                        else:
                            print(f"❌ Línea {lineno}: Elemento inválido en lista: {tokens[j][1]}")
                            break
                        j += 1
                    if j == n or tokens[j][0] != "RBRACE":
                        print(f"❌ Línea {lineno}: Lista no cerrada con '}}'.")
                        break
                    ok, msg = check_list_homogeneity(elements)
                    if not ok:
                        print(f"❌ Línea {lineno}: {msg}")
                        break
                    
                    print("✅ LISTA válida.")
                else:
                    print(f"❌ Línea {lineno}: Valor inválido para variable.")
                    break
            else:
                print(f"❌ Línea {lineno}: Falta '=' en declaración de variable.")
                break

        # Verificar estructuras como if, while, for
        elif kind == "IDENTIFIER" and value in ("if", "while", "for"):
            # Validar paréntesis
            if i+1 >= n or tokens[i+1][0] != "LPAREN":
                print(f"❌ Línea {lineno}: Falta paréntesis de condición en '{value}'.")
                break
            paren = 1
            j = i+2
            while j < n and paren > 0:
                if tokens[j][0] == "LPAREN":
                    paren += 1
                elif tokens[j][0] == "RPAREN":
                    paren -= 1
                j += 1
            if paren != 0:
                print(f"❌ Línea {lineno}: Paréntesis de condición no cerrado en '{value}'.")
                break
            # Debe seguir llave
            while j < n and tokens[j][0] == "WS":
                j += 1
            if j >= n or tokens[j][0] != "LBRACE":
                print(f"❌ Línea {lineno}: Falta '{{' después de condición en '{value}'.")
                break
            
            print(f"✅ Línea {lineno}: ESTRUCTURA {value} válido.")
        
        elif kind == "IDENTIFIER" and value == "else":
            j = i + 1
            if j >= n or tokens[j][0] != "LBRACE":
                print(f"❌ Línea {lineno}: Falta '{{' después de '{value}'.")
                break
            
            print(f"✅ {value} válido.")


        elif kind == "IDENTIFIER":
            valid, msg = is_valid_identifier(value)
            if not valid:
                print(f"❌ Línea {lineno}: {msg}")
                break
            
            print(f"✅ IDENTIFIER válido.")

        elif kind == "OPERATOR":
            if value in BAD_OPERATORS:
                print(f"❌ Línea {lineno}: Operador mal formado '{value}'.")
                break

        elif kind == "UNKNOWN":
            print(f"❌ Línea {lineno}: Carácter no válido '{value}'.")
            break

        i += 1

# Abre el archivo y omite comentarios multilínea
def analyze_file(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            contenido = f.read()

        # Omite comentarios multilínea
        contenido_limpio, num_bloques = extraer_y_marcar_comentarios_multilinea(contenido)
        for _ in range(num_bloques):
            print("🟡 Bloque de comentario ignorado (multilínea)")

        brace_stack = []

        # Recorre linea por linea
        for num_linea, linea in enumerate(contenido_limpio.splitlines(), 1):
            # Verifica si hay llaves sin cerrar
            for c in linea:
                if c == '{':
                    brace_stack.append(num_linea)
                elif c == '}':
                    if not brace_stack:
                        print(f"❌ Línea {num_linea}: Llave '}}' sin abrir.")
                    else:
                        brace_stack.pop()
                        
            # Se llama a analyze_line() para cada línea con contenido
            if linea.strip():
                analyze_line(linea, num_linea)

        for l in brace_stack:
            print(f"❌ Línea {l}: Llave '{{' sin cerrar.")

    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{filename}'")

# ----------- USO -----------
# Ejecutar: python analizador_cereza.py archivo.cereza
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("python analizador_cereza.py archivo.cereza")
    else:
        analyze_file(sys.argv[1])