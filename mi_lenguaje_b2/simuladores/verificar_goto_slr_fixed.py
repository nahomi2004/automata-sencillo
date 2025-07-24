
import pandas as pd
import math

def cargar_tabla_slr(ruta_csv, separador=";"):
    return pd.read_csv(ruta_csv, sep=separador)

def validar_goto(tabla, columnas_ir_a):
    errores = []
    estados_validos = set(str(e) for e in tabla['Estado'])

    for i, fila in tabla.iterrows():
        estado_actual = str(fila['Estado'])
        for col in columnas_ir_a:
            destino = fila[col]
            if pd.isna(destino) or str(destino).strip() == "":
                continue  # Ignorar celdas vacías
            destino_str = str(destino).strip()
            if destino_str not in estados_validos:
                errores.append((estado_actual, col, destino_str))
    return errores

def main():
    ruta_csv = "../csv/Tabla_SLR_-_Base2.csv"  # Cambia esto por el nombre de tu archivo
    tabla = cargar_tabla_slr(ruta_csv)

    columnas = list(tabla.columns)
    columnas_ir_a = [col for col in columnas if col not in ['Estado'] and not col.islower()]

    errores = validar_goto(tabla, columnas_ir_a)

    if errores:
        print("❌ GOTO inválido detectado:")
        for estado, simbolo, destino in errores:
            print(f"Estado {estado}, símbolo '{simbolo}' → destino inválido: '{destino}'")
    else:
        print("✅ Todos los GOTO apuntan a estados válidos.")

if __name__ == "__main__":
    main()
