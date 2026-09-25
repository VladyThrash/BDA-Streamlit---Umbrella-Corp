-- Vladimir Yepez Contreras - IINF - S23002520.

-- TERMINAR ESTO, QUE SE PUEDA SELECIONAR LA RAIZ DEL ARBOL DE JERARQUIAS (Ya).

WITH RECURSIVE cadena_mando as (
    -- Caso base, la raíz del arbol.
    SELECT 
        id_empleado,
        nombre_empleado, 
        apellido_empleado,
        nivel_autorizacion,
        superior_id,
        1 as profundidad
    FROM
        personal
    WHERE
        id_empleado = 11   -- Para empezar desde ese empleado (nodo raiz) hasta las ramas (subordinados).

    UNION ALL

    -- Paso recursivo.
    SELECT
        empleado.id_empleado,
        empleado.nombre_empleado,
        empleado.apellido_empleado,
        empleado.nivel_autorizacion,
        empleado.superior_id,
        cadena_mando.profundidad + 1
    FROM
        personal empleado
    INNER JOIN
        cadena_mando on empleado.superior_id = cadena_mando.id_empleado
)

select id_empleado, nombre_empleado as empleado_final, apellido_empleado, nivel_autorizacion, superior_id, profundidad from cadena_mando
ORDER BY profundidad, empleado_final;