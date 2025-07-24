## Tomar en cuenta

> $ se usa para la entrada final en la tabla acción, pero no forma parte de los items LR(0).

# PRIMEROS

| No Terminal | PRIMEROS                     |
| ----------- | ---------------------------- |
| `PROGRAMA'` | `var, if, while`             |
| `PROGRAMA`  | `var, if, while`             |
| `BLOQUE`    | `var, if, while`             |
| `SENTENCIA` | `var, if, while`             |
| `DECL_VAR`  | `var`                        |
| `IF`        | `if`                         |
| `WHILE`     | `while`                      |
| `COND`      | `id`                         |
| `EXPR`      | `number, id, (`              |
| `TERM`      | `number, id, (`              |
| `FACTOR`    | `number, id, (`              |

# SIGUIENTES

| No Terminal | SIGUIENTE                                                   |
| ----------- | ----------------------------------------------------------- |
| `PROGRAMA'` | `$`                                                         |
| `PROGRAMA`  | `$`                                                         |
| `BLOQUE`    | `}`, `$`                                                    |
| `SENTENCIA` | `;`                                                         |
| `DECL_VAR`  | `;`                                                         |
| `IF`        | `;`                                                         |
| `WHILE`     | `;`                                                         |
| `COND`      | `)`                                                         |
| `EXPR`      | `)`, `;`                                                    |
| `TERM`      | `+`, `-`, `)`, `;`                                          |
| `FACTOR`    | `*`, `/`, `+`, `-`, `)`, `;`                                |
