
# 🍒 Lenguaje de Programación Cereza — Especificación Léxica

Cereza es un lenguaje de programación simple y didáctico inspirado en Python y C, diseñado para prácticas académicas. Su estructura busca combinar tabulaciones y llaves para organizar el flujo del código, permitiendo desarrollar lógica básica, condiciones, ciclos y manipulación de datos simples.

---

## 📌 Estructura general del lenguaje

- Las líneas de código terminan con un salto de línea (`\n`), no se requiere `;` al final.
- Si un `;` se encuentra al final de una línea, será ignorado y se emitirá una advertencia.
- Los bloques se pueden estructurar mediante:
  - **Tabulaciones** (como en Python).
  - **Llaves `{}`** (como en C/C++).
- Si no se usa ni tabulación ni llaves tras estructuras como `if`, `while`, `for`, se marcará **error**.

---

## 🔠 Reglas para nombres de variables

- Las variables se declaran usando la palabra clave `var`.
- Deben iniciar con una letra (mayúscula o minúscula).
- Pueden contener letras y números, los guiones bajos `_` o guiones `-` no son válidos

Ejemplos válidos:
```txt
var edad = 25
var edad3 = 25
var Edad3 = 25
```

Ejemplos inválidos:
```txt
var _variable  ❌
var -nombre    ❌
var nom@bre    ❌
var 9inicio    ❌
```

---

## 🔢 Tipos de datos permitidos

| Tipo        | Forma válida | Ejemplo                  |
|-------------|--------------|---------------------------|
| Entero      | Dígitos       | `12`, `0`, `-45`         |
| Decimal     | Dígitos con punto | `3.14`, `-0.5`        |
| Cadena      | Entre comillas simples o dobles | `"hola"`, `'texto'` |
| Booleano    | `true` o `false` | `true`               |
| Lista       | Entre llaves, homogénea | `{1; 2; 3}`, `{"a"; "b"}` |

---

## ➕ Operadores

### Aritméticos

| Operador | Significado     |
|----------|------------------|
| `+`      | Suma             |
| `-`      | Resta            |
| `*`      | Multiplicación   |
| `/`      | División         |
| `%`      | Módulo           |

### Relacionales

| Operador | Significado        | Notas                     |
|----------|--------------------|---------------------------|
| `==`     | Igual a            | ✅ Válido                  |
| `!=`     | Diferente de       | ✅ Válido                  |
| `>`      | Mayor que          | ✅                        |
| `<`      | Menor que          | ✅                        |
| `>=`     | Mayor o igual que  | ✅                        |
| `=>`     | ❌ No reconocido   | ❌ Error                  |
| `<=`     | Menor o igual que  | ✅                        |

### Lógicos

| Operador | Significado |
|----------|------------|
| `&&` o `&` | AND       |
| `||` o `|` | OR        |

### Incrementales y compuestos

| Operador | Acción                          |
|----------|----------------------------------|
| `++`     | Incrementa en 1                  |
| `--`     | Incrementa en 2                  |

---

## 🔁 Condicionales y ciclos

### Condicionales

```txt
if (<condición>) {
    <instrucciones>
}
else {
    <instrucciones>
}
```

### Ciclos

```txt
while (<condición>) {
    <instrucciones>
}hile (<condición>)

for (<inicialización>, <condición>, <incremento>) {
    <instrucciones>
}
```

---

## ❗ Estructura de condiciones

Solo se permiten condiciones del tipo:

```
<variable> <operador> <variable>
```

O múltiples:

```
<variable> <operador> <variable> <operador_logico> <variable> <operador> <variable>
```

---

## 💬 Comentarios

| Forma       | Tipo        |
|-------------|-------------|
| `# texto`   | Una línea   |
| `/* texto */`   | Multilínea |

---

## 🔐 Palabras reservadas

No pueden usarse como nombres de variables:

```txt
var, if, else, while, for, true, false
```

---

## ⚠️ Advertencias comunes

| Situación                          | Acción              |
|-----------------------------------|---------------------|
| Uso de `;` al final de línea      | Ignorado con aviso  |
| Separación de operadores `= =`    | Advertencia         |
| Operadores mal formados (`=>`)    | Error               |
| Comentarios mal cerrados          | Error               |
| Llaves o paréntesis faltantes     | Error               |

---

## ❌ Errores comunes

| Error                             | Descripción                             |
|----------------------------------|-----------------------------------------|
| `- 9`                            | Espacio entre `-` y número no permitido |
| `var1@`                          | Carácter no válido en variable          |
| `if condicion`                   | Falta paréntesis                        |

---
