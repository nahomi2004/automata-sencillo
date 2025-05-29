import re

# Palabras reservadas
RESERVED = {"var", "if", "else", "while", "for", "true", "false"}

# Operadores válidos y mal formados
BAD_OPERATORS = {'=>', '=<', '==>', '<==', '===', '!==', '->', '<-', '><'}
SEPARATED_EQ = re.compile(r"= =")

# Expresiones regulares para tokens
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

TOKEN_RE = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_REGEX)
)

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

def is_valid_identifier(name):
    if name in RESERVED:
        return False, "No puede usar palabra reservada como identificador."
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", name):
        if re.match(r"^[0-9]", name):
            return False, "Identificador no puede comenzar con número."
        if re.match(r"^_", name):
            return False, "Identificador no puede comenzar con guion bajo."
        if re.match(r"^-", name):
            return False, "Identificador no puede comenzar con guion."
        if " " in name:
            return False, "Identificador no puede contener espacios."
        if re.search(r"[^a-zA-Z0-9]", name):
            return False, "Identificador contiene caracteres inválidos."
        return False, "Identificador inválido."
    return True, ""

def check_list_homogeneity(elements):
    types = set()
    for e in elements:
        if re.fullmatch(r"-?\d+", e):
            types.add("int")
        elif re.fullmatch(r"-?\d+\.\d+", e):
            types.add("float")
        elif e in ("true", "false"):
            types.add("bool")
        elif re.fullmatch(r"(['\"])(?:\\.|(?!\1).)*\1", e):
            types.add("string")
        else:
            return False, f"Elemento inválido en lista: {e}"
    return len(types) == 1, f"Lista no homogénea: contiene tipos {types}"

def extraer_y_marcar_comentarios_multilinea(texto):
    # Detectar comentarios multilínea no cerrados
    if texto.count("/*") != texto.count("*/"):
        print("❌ Comentario de bloque no cerrado.")
    bloques = re.findall(r"/\*.*?\*/", texto, re.DOTALL)
    texto_limpio = re.sub(r"/\*.*?\*/", "", texto, flags=re.DOTALL)
    return texto_limpio, len(bloques)

def analyze_line(line, lineno):
    # Comentario de línea
    if line.strip().startswith("#"):
        return  # Ignorar línea completa

    # Advertencia por punto y coma al final
    if line.strip().endswith(";"):
        print(f"⚠️  Línea {lineno}: ';' al final de línea es ignorado.")
        line = line.rstrip(";")

    # Detectar operadores mal formados
    if SEPARATED_EQ.search(line):
        print(f"⚠️  Línea {lineno}: Operadores '=' separados. Use '=='.")

    for bad in BAD_OPERATORS:
        if bad in line:
            print(f"❌ Línea {lineno}: Operador mal formado '{bad}'.")
            return

    tokens = tokenize(line)
    n = len(tokens)
    i = 0

    while i < n:
        kind, value = tokens[i]

        if kind == "IDENTIFIER" and value == "var":
            if i+1 >= n:
                print(f"❌ Línea {lineno}: Falta identificador en declaración de variable.")
                break
            id_kind, id_value = tokens[i+1]
            valid, msg = is_valid_identifier(id_value)
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
                elif val_kind == "STRING":
                    pass
                elif val_kind == "BOOLEAN":
                    pass
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
                else:
                    print(f"❌ Línea {lineno}: Valor inválido para variable.")
                    break
            else:
                print(f"❌ Línea {lineno}: Falta '=' en declaración de variable.")
                break

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
        
        elif kind == "IDENTIFIER" and value == "else":
            j = i + 1
            if j >= n or tokens[j][0] != "LBRACE":
                print(f"❌ Línea {lineno}: Falta '{{' después de '{value}'.")
                break


        elif kind == "IDENTIFIER":
            valid, msg = is_valid_identifier(value)
            if not valid:
                print(f"❌ Línea {lineno}: {msg}")
                break

        elif kind == "OPERATOR":
            if value in BAD_OPERATORS:
                print(f"❌ Línea {lineno}: Operador mal formado '{value}'.")
                break

        elif kind == "UNKNOWN":
            print(f"❌ Línea {lineno}: Carácter no válido '{value}'.")
            break

        i += 1

def analyze_file(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            contenido = f.read()

        contenido_limpio, num_bloques = extraer_y_marcar_comentarios_multilinea(contenido)
        for _ in range(num_bloques):
            print("🟡 Bloque de comentario ignorado (multilínea)")

        brace_stack = []

        for num_linea, linea in enumerate(contenido_limpio.splitlines(), 1):
            # Balance global de llaves
            for c in linea:
                if c == '{':
                    brace_stack.append(num_linea)
                elif c == '}':
                    if not brace_stack:
                        print(f"❌ Línea {num_linea}: Llave '}}' sin abrir.")
                    else:
                        brace_stack.pop()

            if linea.strip():
                analyze_line(linea, num_linea)

        for l in brace_stack:
            print(f"❌ Línea {l}: Llave '{{' sin cerrar.")

    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{filename}'")

# ----------- USO -----------
# Guarda este script como analizador_cereza.py
# Ejecuta con: python analizador_cereza.py archivo.cereza

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python analizador_cereza.py archivo.cereza")
    else:
        analyze_file(sys.argv[1])