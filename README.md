
# 🍒 Lenguaje de Programación Cereza — Especificación Léxica

Cereza es un lenguaje de programación simple y didáctico inspirado en Python y C, diseñado para prácticas académicas. Su estructura busca combinar tabulaciones y llaves para organizar el flujo del código, permitiendo desarrollar lógica básica, condiciones, ciclos y manipulación de datos simples.

---

## 📌 Estructura general del lenguaje

- Las líneas de código terminan con un salto de línea (`\n`), no se requiere `;` al final.
- Los bloques se pueden estructurar mediante:
  - **Llaves `{}`** (como en C/C++).
- Si no se usa llaves tras estructuras como `if`, `while`, se marcará **error**.

---

## 🔠 Reglas para nombres de variables

- Las variables se declaran usando la palabra clave `var`.
- Deben iniciar con una letra (mayúscula o minúscula).
- No pueden contener números, ni guiones bajos `_` o guiones `-`.

Ejemplos válidos:
```txt
var edad = 25
var Edad = 25
var edaD = 25
```

Ejemplos inválidos:
```txt
var _variable  ❌
var -nombre    ❌
var nom@bre    ❌
var x3    ❌
```

---

## 🔢 Tipos de datos permitidos

| Tipo        | Forma válida | Ejemplo                  |
|-------------|--------------|---------------------------|
| Entero      | Dígitos       | `12`, `0`, `-45`         |
| Decimal     | Dígitos con punto | `3.14`, `-0.5`        |
| Cadena      | Entre comillas dobles | `"hola"` |
| Booleano    | `true` o `false` | `true`               |
| Lista       | Entre llaves, homogéneas numericas | `{1, 2, 3}` |

---

## ➕ Operadores

### Aritméticos

| Operador | Significado     |
|----------|------------------|
| `+`      | Suma             |
| `-`      | Resta            |
| `*`      | Multiplicación   |
| `/`      | División         |

### Relacionales

| Operador | Significado        | Notas                     |
|----------|--------------------|---------------------------|
| `==`     | Igual a            | ✅ Válido                  |
| `!=`     | Diferente de       | ✅ Válido                  |
| `>`      | Mayor que          | ✅                        |
| `<`      | Menor que          | ✅                        

### Incrementales y compuestos

| Operador | Acción                          |
|----------|----------------------------------|
| `++`     | Incrementa en 1                  |
| `--`     | Decrementa en 1                  |

---

## 🔁 Condicionales y ciclos

### Condicionales

```txt
if (<condición>) {
    <instrucciones>
}
```

### Ciclos

```txt
while (<condición>) {
    <instrucciones>
}
```

---

## ❗ Estructura de condiciones

Solo se permiten condiciones del tipo:

```
<variable> <operador relacional> <variable>
```

---

## 💬 Comentarios

| Forma       | Tipo        |
|-------------|-------------|
| `# texto`   | Una línea   |

---

## 🔐 Palabras reservadas

No pueden usarse como nombres de variables:

```txt
var, if, while, true, false
```

---

## ❌ Errores comunes

| Error                             | Descripción                            |
|----------------------------------|-----------------------------------------|
| `- 9`                            | Espacio entre `-` y número no permitido |
| `var1@`                          | Carácter no válido en variable          |
| `if condicion`                   | Falta paréntesis                        |
| Operadores mal formados (`=>`)    | Error                                  |
| Llaves o paréntesis faltantes     | Error                                  |

---
