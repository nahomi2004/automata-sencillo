<PROGRAMA> -> <BLOQUE DE CODIGO>

<BLOQUE DE CODIGO> -> <SENTENCIA>
<BLOQUE DE CODIGO> -> <SENTENCIA> <BLOQUE DE CODIGO>

<SENTENCIA> -> <DECLARACION VARIABLE>
<SENTENCIA> -> <WHILE>
<SENTENCIA> -> <IF>
<SENTENCIA> -> id ++
<SENTENCIA> -> id --

<DECLARACION VARIABLE> -> var id = <EXPR>
<DECLARACION VARIABLE> -> var id = boolean
<DECLARACION VARIABLE> -> var id = string
<DECLARACION VARIABLE> -> var id = <LISTA>

<LISTA> -> {<VALOR LISTA>}
<VALOR LISTA> -> number
<VALOR LISTA> -> number , <VALOR LISTA>

<WHILE> -> while ( <CONDICION> ) { <BLOQUE DE CODIGO> }
<IF> -> if ( <CONDICION> ) { <BLOQUE DE CODIGO> }

<CONDICION> -> id == id
<CONDICION> -> id != id
<CONDICION> -> id > id
<CONDICION> -> id < id

# --- Expresiones con orden de prioridad ---

<EXPR> -> <TERM> + <EXPR>
<EXPR> -> <TERM> - <EXPR>
<EXPR> -> <TERM>

<TERM> -> <FACTOR> * <TERM>
<TERM> -> <FACTOR> / <TERM>
<TERM> -> <FACTOR>

<FACTOR> -> number
<FACTOR> -> id
<FACTOR> -> (<EXPR>)