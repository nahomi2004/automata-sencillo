
import pandas as pd

# Cargar la tabla SLR
slr_table = pd.read_csv("Tabla_SLR_-_Base.csv", delimiter=";").fillna("").astype(str)
slr_table['Estado'] = slr_table['Estado'].astype(int)

# Cadena de entrada tokenizada
input_tokens = ['var', 'id', '=', 'number', '*', 'number', '$']

# Inicialización
stack = [0]
input_pointer = 0
actions = []

# Producciones con su número
productions = {
    7: ['var', 'id', '=', 'E'],
    14: ['T', '+', 'E'],
    15: ['T', '-', 'E'],
    16: ['T'],
    17: ['F', '*', 'T'],
    18: ['F', '/', 'T'],
    19: ['F'],
    20: ['number'],
    21: ['id'],
    22: ['(', 'E', ')']
}

# LHS de producciones
lhs_map = {
    7: 'D',
    14: 'E',
    15: 'E',
    16: 'E',
    17: 'T',
    18: 'T',
    19: 'T',
    20: 'F',
    21: 'F',
    22: 'F'
}

# Simulación
while True:
    state = stack[-1]
    token = input_tokens[input_pointer]

    action_row = slr_table[slr_table['Estado'] == state]
    if action_row.empty or token not in action_row.columns:
        print(f"[ERROR] Estado: {state}, Token: {token} → Acción no encontrada.")
        break

    action = action_row[token].values[0]
    print(f"Pila: {stack}, Entrada: {' '.join(input_tokens[input_pointer:])}, Acción: {action}")

    if action == 'accept':
        print("✅ Cadena aceptada")
        break

    if action == '':
        print("❌ Error de análisis")
        break

    if action.startswith('s'):
        stack.append(token)
        stack.append(int(action[1:]))
        input_pointer += 1

    elif action.startswith('r'):
        prod_num = int(action[1:])
        rhs = productions.get(prod_num, [])
        for _ in range(len(rhs) * 2):
            stack.pop()
        current_state = stack[-1]
        lhs = lhs_map[prod_num]
        stack.append(lhs)
        goto_state = slr_table.loc[slr_table['Estado'] == current_state, lhs].values[0]
        if goto_state == '':
            print("❌ Error: GOTO no definido")
            break
        stack.append(int(goto_state))
