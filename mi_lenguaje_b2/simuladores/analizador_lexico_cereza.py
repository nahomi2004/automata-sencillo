import re

# === 🍒 Analizador Léxico para el Lenguaje Cereza ===

RESERVED = {"var", "if", "while"}

BAD_OPERATORS = {"=>", "=<", "==>", "<==", "===", "!==", "->", "<-", "><"}
SEPARATED_EQ = re.compile(r"= =")

TOKEN_REGEX = [
    ("COMMENT_LINE", r"#.*"),
    ("NUMBER", r"-?\d+"),
    ("EQ", r"=="),
    ("NEQ", r"!="),
    ("GE", r">="),
    ("LE", r"<="),
    ("GT", r">"),
    ("LT", r"<"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULT", r"\*"),
    ("DIV", r"/"),
    ("ASSIGN", r"="),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("ID", r"[a-zA-Z_][a-zA-Z_0-9]*"),
    ("WS", r"\s+"),
    ("UNKNOWN", r".")
]

TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_REGEX))

def tokenize_line(line, lineno):
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
        elif kind == "ID" and value in RESERVED:
            tokens.append(("✅ RESERVED", value))
        elif kind == "ID":
            tokens.append(("✅ IDENTIFIER", value))
        else:
            tokens.append(("✅", kind, value))

        pos = match.end()

    return tokens

def analizador_lexico_cereza(texto):
    resultados = []
    lineas = texto.splitlines()
    for num, linea in enumerate(lineas, 1):
        if linea.strip().startswith("#") or not linea.strip():
            continue
        resultado = tokenize_line(linea, num)
        resultados.append((num, resultado))
    return resultados
