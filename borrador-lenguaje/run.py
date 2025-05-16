import re

# Definición de patrones
token_patterns = {
    "NUMBER": r"\b\d+(\.\d+)?\b",
    "OPERATOR": r"[\+\-\*/]",
    "COMPARATOR": r"(==|!=|<=|>=|<|>)",
    "ASSIGNMENT": r"=",
    "VARIABLE": r"\b[a-zA-Z_]\w*\b"
}

def tokenize(line):
    tokens = []
    for token in line.strip().split():
        matched = False
        for token_type, pattern in token_patterns.items():
            if re.fullmatch(pattern, token):
                tokens.append((token_type, token))
                matched = True
                break
        if not matched:
            tokens.append(("ERROR", token))
    return tokens

# Leer archivo
filename = "programa.txt"
try:
    with open(filename, 'r') as file:
        for line_num, line in enumerate(file, 1):
            print(f"\nLínea {line_num}: {line.strip()}")
            tokens = tokenize(line)
            for token_type, token in tokens:
                if token_type == "ERROR":
                    print(f"❌ Error: '{token}' no es un token válido.")
                else:
                    print(f"✅ {token} → {token_type}")
except FileNotFoundError:
    print(f"No se encontró el archivo '{filename}'.")
