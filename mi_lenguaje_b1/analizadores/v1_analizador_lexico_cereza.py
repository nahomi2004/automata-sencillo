import re

# === Definición de patrones para tokens ===
token_specs = [
    ("COMMENT_MULTI", r"('''.*?'''|/\*.*?\*/)", re.DOTALL),
    ("COMMENT_SINGLE", r"(#.*|//.*)"),
    ("BOOLEAN", r"\b(true|false)\b"),
    ("KEYWORD", r"\b(var|if|else|elseif|while|for|in|do)\b"),
    ("IDENTIFIER", r"\b[a-zA-Z]([a-zA-Z0-9]*[-_]?[a-zA-Z0-9]+)*\b"),
    ("NUMBER_FLOAT", r"-?\d+\.\d+"),
    ("NUMBER_INT", r"-?\d+\b"),
    ("STRING", r"\".*?\"|'.*?'"),
    ("OP_INC", r"(\+\+|--|\+=|=+|-=|=-|\*=|=\*|/=|=/)"),
    ("OP_REL", r"(==|!=|=!|=<|>=|<|>)"),
    ("OP_LOGIC", r"(\|\||\||&&|&)"),
    ("OP_ARITH", r"[\+\-\*/%]"),
    ("GROUP", r"[{}\[\]()]"),
    ("DELIMITER", r";"),  # genera advertencia
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r".")
]

# Compilamos todos los patrones en una expresión regular maestra
tok_regex = '|'.join(f"(?P<{name}>{pattern})" for name, pattern, *_ in token_specs)

# === Función para analizar líneas de un archivo ===
def analizar_linea(linea, num_linea):
    for mo in re.finditer(tok_regex, linea):
        tipo = mo.lastgroup
        valor = mo.group()
        
        if tipo == "SKIP" or tipo == "NEWLINE":
            continue
        elif tipo == "DELIMITER":
            print(f"⚠️ Línea {num_linea}: Se encontró ';' (no es necesario).")
        elif tipo == "MISMATCH":
            print(f"❌ Línea {num_linea}: Carácter inesperado '{valor}'")
        elif tipo == "COMMENT_SINGLE" or tipo == "COMMENT_MULTI":
            print(f"🟡 Línea {num_linea}: Comentario ignorado")
        else:
            print(f"✅ Línea {num_linea}: Token válido → {tipo}: {valor}")

# === Función principal para leer y analizar un archivo ===
def analizar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for i, linea in enumerate(archivo, 1):
                analizar_linea(linea, i)
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{nombre_archivo}'")

# === Ejecutar ===
if __name__ == "__main__":
    archivo_fuente = "..\programas\programa_cereza.txt"
    analizar_archivo(archivo_fuente)
