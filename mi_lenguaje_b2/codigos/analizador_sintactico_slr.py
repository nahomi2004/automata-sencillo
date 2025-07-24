import csv
from lexico import analizador_lexico_cereza

def cargar_tabla_slr(archivo_csv):
    """Carga la tabla SLR desde un archivo CSV"""
    tabla_accion = {}
    tabla_goto = {}
    
    with open(archivo_csv, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=';')
        encabezados = next(lector)
        
        # Identificar columnas de terminales y no terminales
        terminales = [';', 'var', 'id', '=', '+', '-', '*', '/', 'NUMBER', 'if', 'while', 
                        '(', ')', '{', '}', '==', '!=', '>', '<', '$']
        no_terminales = ['P\'', 'P', 'B', 'S', 'D', 'I', 'W', 'C', 'E', 'T', 'F']
        
        for fila in lector:
            estado = int(fila[0])
            tabla_accion[estado] = {}
            tabla_goto[estado] = {}
            
            # Procesar acciones (terminales)
            for i, terminal in enumerate(terminales, 1):
                if i < len(fila) and fila[i]:
                    celda = fila[i].strip()
                    if celda == 'accept':
                        tabla_accion[estado][terminal] = 'accept'
                    elif celda.startswith('s'):
                        # Desplazar
                        estado_destino = int(celda[1:])
                        tabla_accion[estado][terminal] = ('s', estado_destino)
                    elif celda.startswith('r'):
                        # Reducir
                        produccion = int(celda[1:])
                        tabla_accion[estado][terminal] = ('r', produccion)
                else:
                    tabla_accion[estado][terminal] = None
            
            # Procesar transiciones GOTO (no terminales)
            inicio_nt = len(terminales) + 1
            for i, no_terminal in enumerate(no_terminales):
                indice = inicio_nt + i
                if indice < len(fila) and fila[indice]:
                    estado_destino = int(fila[indice])
                    tabla_goto[estado][no_terminal] = estado_destino
                else:
                    tabla_goto[estado][no_terminal] = None
    
    return tabla_accion, tabla_goto

def obtener_produccion(numero):
    """Devuelve la producción correspondiente al número"""
    # Reordenando las producciones según la tabla CSV
    producciones = {
        1: ("P", ["B"]),                    # P -> B
        2: ("B", ["S", ";"]),               # B -> S;
        3: ("B", ["S", ";", "B"]),          # B -> S; B
        4: ("S", ["D"]),                    # S -> D
        5: ("S", ["I"]),                    # S -> I
        6: ("S", ["W"]),                    # S -> W
        7: ("D", ["var", "id", "=", "E"]),  # D -> var id = E
        8: ("I", ["if", "(", "C", ")", "{", "B", "}"]),    # I -> if ( C ) { B }
        9: ("W", ["while", "(", "C", ")", "{", "B", "}"]), # W -> while ( C ) { B }
        10: ("C", ["id", "==", "id"]),      # C -> id == id
        11: ("C", ["id", "!=", "id"]),      # C -> id != id
        12: ("C", ["id", ">", "id"]),       # C -> id > id
        13: ("C", ["id", "<", "id"]),       # C -> id < id
        14: ("E", ["T", "+", "E"]),         # E -> T + E
        15: ("E", ["T", "-", "E"]),         # E -> T - E
        16: ("E", ["T"]),                   # E -> T
        17: ("T", ["F", "*", "T"]),         # T -> F * T
        18: ("T", ["F", "/", "T"]),         # T -> F / T
        19: ("T", ["F"]),                   # T -> F
        20: ("F", ["NUMBER"]),              # F -> NUMBER
        21: ("F", ["id"]),                  # F -> id
        22: ("F", ["(", "E", ")"])          # F -> ( E )
    }
    return producciones.get(numero, (None, []))

def mapear_token_a_terminal(token):
    """Mapea los tokens del analizador léxico a los terminales de la gramática"""
    if len(token) == 3:  # Tokens como ("✅", "PLUS", "+")
        estado, tipo, valor = token
        if estado == "✅":
            if tipo == "IDENTIFIER":
                return "id"
            elif tipo == "NUMBER":
                return "NUMBER"
            elif valor in ['{', '}', '(', ')', ';', '+', '-', '*', '/', '=', '==', '!=', '>', '<']:
                return valor
            elif tipo == "RESERVED" and valor in ["var", "if", "while"]:
                return valor
    elif len(token) == 2:  # Tokens como ("✅ RESERVED", "var") o ("✅ IDENTIFIER", "x")
        tipo_completo, valor = token
        if tipo_completo == "✅ RESERVED":
            return valor  # var, if, while
        elif tipo_completo == "✅ IDENTIFIER":
            return "id"
    
    return None

def simular_parser(codigo, archivo_tabla_csv):
    """Simula el analizador sintáctico SLR"""
    # Cargar tabla SLR
    tabla_accion, tabla_goto = cargar_tabla_slr(archivo_tabla_csv)
    
    # Obtener tokens del analizador léxico
    tokens_por_linea = analizador_lexico_cereza(codigo)
    tokens = []
    
    print("🔍 Tokens del analizador léxico:")
    for linea, tokens_linea in tokens_por_linea:
        print(f"Línea {linea}: {tokens_linea}")
        for token in tokens_linea:
            # Verificar si hay errores
            if len(token) >= 2 and "ERROR" in token[0]:
                print(f"❌ Error léxico: {token}")
                return False
            
            # Mapear token a terminal
            terminal = mapear_token_a_terminal(token)
            if terminal:
                tokens.append(terminal)
                # print(f"  {token} -> {terminal}") # Imprimir por individual los elementos de la linea lexica
    
    # Agregar símbolo de fin de cadena
    tokens.append('$')
    
    # Inicializar pila y puntero de entrada
    pila = [0]  # Estado inicial
    ae = 0  # Apuntador de entrada
    producciones_aplicadas = []
    
    print(f"\n🎯 Tokens a analizar: {tokens}")
    print("🚀 Iniciando análisis sintáctico...\n")
    
    paso = 1
    while True:
        # Estado en la cima de la pila
        s = pila[-1]
        # Símbolo actual apuntado por ae
        if ae < len(tokens):
            a = tokens[ae]
        else:
            print("❌ Error: Se acabaron los tokens")
            return False
        
        print(f"⚪ Paso {paso}: Estado actual: {s}, Token actual: {a}, Pila: {pila}")
        paso += 1
        
        # Verificar acción en la tabla
        if s not in tabla_accion or a not in tabla_accion[s]:
            print(f"❌ Error: No hay acción definida para estado {s} y token {a}")
            return False
        
        accion = tabla_accion[s][a]
        
        if accion is None:
            print(f"❌ Error sintáctico en estado {s} con token {a}")
            return False
        
        elif accion == 'accept':
            print("🎉 ¡Análisis sintáctico exitoso!")
            print("\n📋 Producciones aplicadas:")
            for i, prod in enumerate(producciones_aplicadas, 1):
                print(f"{i}. {prod[0]} -> {' '.join(prod[1])}")
            return True
        
        elif accion[0] == 's':  # Desplazar
            estado_destino = accion[1]
            print(f"➡️ Desplazar a estado {estado_destino}")
            pila.append(a)  # Meter símbolo
            pila.append(estado_destino)  # Meter estado
            ae += 1  # Avanzar al siguiente token
        
        elif accion[0] == 'r':  # Reducir
            produccion_num = accion[1]
            izq, der = obtener_produccion(produccion_num)
            
            if izq is None:
                print(f"❌ Error: Producción {produccion_num} no encontrada")
                return False
            
            print(f"↩️ Reducir por producción {produccion_num}: {izq} -> {' '.join(der)}")
            producciones_aplicadas.append((izq, der))
            
            # Sacar 2 * |β| símbolos de la pila
            elementos_a_sacar = 2 * len(der)
            print(f"   Sacando {elementos_a_sacar} elementos de la pila")
            for i in range(elementos_a_sacar):
                if pila:
                    elemento = pila.pop()
                    print(f"   Sacando: {elemento}")
            
            # Estado que ahora está en la cima
            if not pila:
                print("❌ Error: Pila vacía después de reducción")
                return False
            
            s_prima = pila[-1]
            print(f"   Estado en la cima después de reducción: {s_prima}")
            
            # Buscar transición GOTO
            if s_prima not in tabla_goto or izq not in tabla_goto[s_prima]:
                print(f"❌ Error: No hay transición GOTO desde estado {s_prima} con {izq}")
                print(f"   Estados disponibles en tabla_goto: {list(tabla_goto.keys())}")
                if s_prima in tabla_goto:
                    print(f"   Símbolos disponibles desde estado {s_prima}: {[k for k, v in tabla_goto[s_prima].items() if v is not None]}")
                return False
            
            estado_goto = tabla_goto[s_prima][izq]
            if estado_goto is None:
                print(f"❌ Error: Transición GOTO no definida desde estado {s_prima} con {izq}")
                return False
            
            print(f"   GOTO({s_prima}, {izq}) = {estado_goto}")
            # Meter A y después ir_a[s', A] en la pila
            pila.append(izq)
            pila.append(estado_goto)
        
        else:
            print(f"❌ Error: Acción desconocida {accion}")
            return False
        
        print()  # Línea en blanco para mejor legibilidad