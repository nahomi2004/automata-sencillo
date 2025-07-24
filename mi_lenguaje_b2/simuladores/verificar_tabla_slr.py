
import pandas as pd

def cargar_tabla_slr(ruta_csv, separador=";"):
    return pd.read_csv(ruta_csv, sep=separador)

def detectar_conflictos(tabla, columnas_accion):
    conflictos = []
    for i, fila in tabla.iterrows():
        for col in columnas_accion:
            celda = str(fila[col]).strip()
            if ',' in celda:  # múltiples acciones en una celda
                conflictos.append((fila['Estado'], col, celda))
            elif celda.startswith('s') and celda.startswith('r'):
                conflictos.append((fila['Estado'], col, celda))
    return conflictos

def main():
    ruta_csv = "../csv/Tabla_SLR_-_Base2.csv"  # Cambia esto por el nombre de tu archivo
    tabla = cargar_tabla_slr(ruta_csv)

    columnas = list(tabla.columns)
    columnas_accion = [col for col in columnas if col not in ['Estado'] and col.islower()]

    conflictos = detectar_conflictos(tabla, columnas_accion)

    if conflictos:
        print("⚠️ Conflictos encontrados en la tabla SLR:")
        for estado, simbolo, accion in conflictos:
            print(f"Estado {estado}, Símbolo '{simbolo}': Acción conflictiva -> {accion}")
    else:
        print("✅ No se encontraron conflictos en la tabla SLR.")

if __name__ == "__main__":
    main()
