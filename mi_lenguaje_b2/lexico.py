import re

# === 🍒 Analizador Léxico para el Lenguaje Cereza ===

# Palabras reservadas del lenguaje
RESERVED = {"var", "if", "else", "while", "for", "true", "false"}

# Operadores mal formados
BAD_OPERATORS = {"=>", "=<", "==>", "<==", "===", "!==", "->", "<-", "><"}
SEPARATED_EQ = re.compile(r"= =")

# Definición de los tipos de tokens
TOKEN_REGEX = [
    ("COMMENT_LINE", r"#.*"),
    ("STRING", r'".*?"|\'.*?\''),
    ("NUMBER", r"-?\d+\.\d+|-?\d+"),
    ("BOOLEAN", r"\btrue\b|\bfalse\b"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMA", r","),
    ("OPERATOR", r"==|!=|<=|>=|\+\+|--|[+\-*/%<>=]"),
    ("IDENTIFIER", r"[a-zA-Z]+"),
    ("WS", r"\s+"),
    ("UNKNOWN", r".")
]

TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_REGEX))

def tokenize_line(line, lineno):
    """Devuelve los tokens reconocidos en una línea o errores si hay símbolos inválidos."""
    tokens = []

    if line.strip().endswith(";"):
        return [("❌ ERROR", lineno, "; al final de línea no es válido")]

    if SEPARATED_EQ.search(line):
        return [("❌ ERROR", lineno, "Uso de '= =' separado. Use '=='")]

    for bad in BAD_OPERATORS:
        if bad in line:
            return [("❌ ERROR", lineno, f"Operador mal formado '{bad}'")] 

    pos = 0
    while pos < len(line):
        match = TOKEN_RE.match(line, pos)
        if not match:
            tokens.append(("❌ ERROR", lineno, f"Símbolo no reconocido: '{line[pos]}'"))
            pos += 1
            continue

        kind = match.lastgroup
        value = match.group()
        if kind == "WS":
            pos = match.end()
            continue

        if kind == "UNKNOWN":
            tokens.append(("❌ ERROR", lineno, f"Carácter no válido: '{value}'"))
        elif kind == "IDENTIFIER" and value in RESERVED:
            tokens.append(("✅ RESERVED", value))
        elif kind == "IDENTIFIER":
            tokens.append(("✅ IDENTIFIER", value))
        else:
            tokens.append(("✅", kind, value))

        pos = match.end()

    return tokens

def analizador_lexico_cereza(texto):
    """Función que tokeniza un texto completo (líneas de código) y retorna lista de tokens o errores."""
    resultados = []
    lineas = texto.splitlines()
    for num, linea in enumerate(lineas, 1):
        if linea.strip().startswith("#") or not linea.strip():
            continue  # ignorar comentarios o líneas vacías
        resultado = tokenize_line(linea, num)
        resultados.append((num, resultado))
    return resultados
