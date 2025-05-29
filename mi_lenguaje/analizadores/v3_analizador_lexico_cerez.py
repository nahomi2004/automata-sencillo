
import re

# === Patrones mejorados con detección de operadores inválidos ===
token_specs_v5 = [
    ("INVALID_REL", r"(=<|=>)"),
    ("BOOLEAN", r"\b(true|false)\b"),
    ("KEYWORD", r"\b(var|if|else|elseif|while|for|in|do)\b"),
    ("IDENTIFIER", r"\b[a-zA-Z]([a-zA-Z0-9]*([-_][a-zA-Z0-9]+)*)?\b"),
    ("NUMBER_FLOAT", r"-?\d+\.\d+"),
    ("NUMBER_INT", r"-?\d+\b"),
    ("STRING", r"\".*?\"|'.*?'"),
    ("OP_INC", r"(\+\+|--|\+=|=\+|-=|=-|\*=|=\*|/=|=/)"),
    ("ASSIGN", r"="),
    ("OP_REL", r"(==|!=|=!|<=|>=|<|>)"),
    ("OP_LOGIC", r"(&&|&|\|\||\|)"),
    ("OP_ARITH", r"[+\-*/%]"),
    ("GROUP", r"[{}\[\]()]"),
    ("DELIMITER", r";"),
    ("COMMENT_SINGLE", r"(#.*)"),
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\n"),
    ("MISMATCH", r".")
]

tok_regex_v5 = '|'.join(f"(?P<{name}>{pattern})" for name, pattern, *_ in token_specs_v5)

def extraer_y_marcar_comentarios_multilinea(texto):
    bloques = []

    if "/*" in texto and "*/" not in texto:
        print("❌ Error: Comentario con /* no cerrado.")
    if '' in texto and texto.count('') % 2 != 0:
        print("❌ Error: Comentario con triple comilla no cerrado.")

    def reemplazo(match):
        bloques.append(match.group())
        return "\n" * match.group().count('\n')

    texto_sin_comentarios = re.sub(r"('''(.|\n)*?'''|/\*(.|\n)*?\*/)", reemplazo, texto)
    return texto_sin_comentarios, len(bloques)

def analizar_linea_v5(linea, num_linea):
    tokens = list(re.finditer(tok_regex_v5, linea))
    i = 0
    encontrado_var = False
    esperando_asignacion = False
    esperando_valor = False

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

        if tipo == "INVALID_REL":
            print(f"❌ Línea {num_linea}: Operador relacional inválido '{valor}'")
            break

        if valor == "var":
            encontrado_var = True
            esperando_asignacion = False
            esperando_valor = False
            print(f"✅ Línea {num_linea}: Palabra clave → {valor}")
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

        if esperando_asignacion:
            if tipo == "ASSIGN":
                print(f"✅ Línea {num_linea}: Operador de asignación detectado")
                esperando_asignacion = False
                esperando_valor = True
            else :
                print(f"❌ Línea {num_linea}: Se esperaba solo '=' como operador de asignación.")
                break
            i += 1
            continue

        if esperando_valor:
            if tipo in ("STRING", "NUMBER_FLOAT", "NUMBER_INT", "BOOLEAN", "IDENTIFIER"):
                print(f"✅ Línea {num_linea}: Valor válido: {valor}")
                esperando_valor = False
                encontrado_var = False
            else:
                print(f"❌ Línea {num_linea}: Valor no válido después de '=' → '{valor}'")
                break
            i += 1
            continue
        
        # Validar estructuras de control (if, while, for, etc.)
        if valor in ("if", "while", "for"):
            if i + 1 >= len(tokens) or tokens[i + 1].group() != "(":
                print(f"❌ Línea {num_linea}: Se esperaba '(' después de '{valor}'.")
                break

        # Validar 'for-in' (estructura especial)
        if valor == "for" and i + 3 < len(tokens):
            tok1 = tokens[i + 1].group()
            tok2 = tokens[i + 2].group()
            tok3 = tokens[i + 3].group()
            if tok2 != "in":
                print(f"❌ Línea {num_linea}: La estructura 'for (x) in (lista)' está mal formada.")
                break

        print(f"✅ Línea {num_linea}: Token válido → {tipo}: {valor}")
        i += 1

def analizar_archivo_v5(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

        contenido_limpio, num_bloques = extraer_y_marcar_comentarios_multilinea(contenido)
        for _ in range(num_bloques):
            print("🟡 Bloque de comentario ignorado (multilínea)")

        for num_linea, linea in enumerate(contenido_limpio.splitlines(), 1):
            if linea.strip():
                analizar_linea_v5(linea, num_linea)

    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{nombre_archivo}'")

if __name__ == "__main__":
    analizar_archivo_v5("..\programas txt\programa_cereza.txt")
