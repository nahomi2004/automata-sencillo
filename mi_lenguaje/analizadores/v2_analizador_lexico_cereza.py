import re

# === Definición de patrones léxicos ===
token_specs_v4 = [
    ("BOOLEAN", r"\b(true|false)\b"),
    ("KEYWORD", r"\b(var|if|else|elseif|while|for|in|do)\b"),
    ("IDENTIFIER", r"\b[a-zA-Z]([a-zA-Z0-9]*([-_][a-zA-Z0-9]+)*)?\b"),
    ("NUMBER_FLOAT", r"-?\d+\.\d+"),
    ("NUMBER_INT", r"-?\d+\b"),
    ("STRING", r"\".*?\"|'.*?'"),
    ("OP_INC", r"(\+\+|--|\+=|=+|-=|=-|\*=|=\*|/=|=/)"),
    ("OP_REL", r"(==|!=|=!|<=|>=|<|>)"),
    ("OP_LOGIC", r"(&&|&|\|\||\|)"),
    ("OP_ARITH", r"[+\-*/%]"),
    ("GROUP", r"[{}\[\]()]"),
    ("DELIMITER", r";"),
    ("COMMENT_SINGLE", r"(#.*|//.*)"),
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\n"),
    ("MISMATCH", r".")
]

tok_regex_v4 = '|'.join(f"(?P<{name}>{pattern})" for name, pattern, *_ in token_specs_v4)

def extraer_y_marcar_comentarios_multilinea(texto):
    bloques = []
    def reemplazo(match):
        bloques.append(match.group())
        return "\n" * match.group().count('\n')  # conserva saltos de línea
    texto_sin_comentarios = re.sub(r"('''(.|\n)*?'''|/\*(.|\n)*?\*/)", reemplazo, texto)
    return texto_sin_comentarios, len(bloques)

def analizar_linea_v4(linea, num_linea):
    tokens = list(re.finditer(tok_regex_v4, linea))
    i = 0
    encontrado_var = False
    esperando_asignacion = False

    while i < len(tokens):
        mo = tokens[i]
        tipo = mo.lastgroup
        valor = mo.group()

        if tipo in ("SKIP", "NEWLINE"):
            i += 1
            continue

        if tipo == "DELIMITER":
            print(f"⚠️ Línea {num_linea}: Se encontró ';' (no es necesario).")
            i += 1
            continue

        if tipo == "COMMENT_SINGLE":
            print(f"🟡 Línea {num_linea}: Comentario ignorado (una línea)")
            break
            
        if tipo == "MISMATCH":
            print(f"❌ Línea {num_linea}: Carácter inesperado '{valor}'")
            break

        if valor == "var":
            encontrado_var = True
            esperando_asignacion = False
            print(f"✅ Línea {num_linea}: Palabra clave → {valor}")
            i += 1
            continue

        if esperando_asignacion:
            if valor == "=":
                print(f"✅ Línea {num_linea}: Operador de asignación detectado")
                break
            else:
                print(f"❌ Línea {num_linea}: Se esperaba '=' después del nombre de variable.")
                break
            i += 1
            continue
        
        if encontrado_var and not esperando_asignacion:
            if tipo != "IDENTIFIER":
                print(f"❌ Línea {num_linea}: Después de 'var' se esperaba un nombre de variable válido.")
                break
            if re.match(r"[-_]", valor[0]):
                print(f"❌ Línea {num_linea}: Nombre de variable no puede iniciar con '-' o '_'.")
                break
            print(f"✅ Línea {num_linea}: Identificador válido: {valor}")
            esperando_asignacion = True
            i += 1
            continue

        print(f"✅ Línea {num_linea}: Token válido → {tipo}: {valor}")
        i += 1

def analizar_archivo_v4(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

        contenido_limpio, num_bloques = extraer_y_marcar_comentarios_multilinea(contenido)
        for _ in range(num_bloques):
            print("🟡 Bloque de comentario ignorado (multilínea)")

        for num_linea, linea in enumerate(contenido_limpio.splitlines(), 1):
            if linea.strip():
                analizar_linea_v4(linea, num_linea)

    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{nombre_archivo}'")

# === Ejecutar ===
if __name__ == "__main__":
    analizar_archivo_v4("..\programas\programa_cereza.txt")
