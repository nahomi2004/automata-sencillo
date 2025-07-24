apuntar ae al primer simbolo de w$; 
repeat forever begin
    sea s el estado en la cima de la pila y
        a el símbolo apuntado por ae;
    if acción [s, a] = desplazar s' then begin
        meter a y después s' en la cima de la pila;
        avanzar ae al siguiente simbolo de entrada
    end
    else if acción [s, a] = reducir A→ ẞ then begin 
        sacar 2* |B| símbolos de la pila;
        sea s' el estado que ahora está en la cima de la pila;
        meter A y después ir_a [s', A] en la cima de la pila; 
        emitir la producción A → B
    end
    else if acción [s, a] = aceptar then
        return
    else error ()
end