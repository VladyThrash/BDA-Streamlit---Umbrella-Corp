-- Vladimir Yepez Contreras - S23002520 - IINF.
-- Aquí vamos a colocar consultas para analizar el funcionamiento y rendimiento de la BD.


-- Vamos a mostrar a todos los B.O.W's indicando si son Zoológicos o Humanoides.
select BOW.codigo_lote, BOW.nombre_clave, BOW.fecha_mutacion, Laboratorio.lab_origen, 'Zoologicas' as Tipo from Zoologicas
join bow on bow.codigo_lote = Zoologicas.lote_codigo
join laboratorio on laboratorio.codigo_laboratorio = bow.laboratorio_codigo
UNION
select BOW.codigo_lote, BOW.nombre_clave, BOW.fecha_mutacion, Laboratorio.nombre_clave, 'Humanoides' as Tipo from Humanoides
join bow on bow.codigo_lote = Humanoides.lote_codigo
join laboratorio on laboratorio.codigo_laboratorio = bow.laboratorio_codigo;


-- Vamos a mostrar a los trabajadores y sus superiores
select empleado.id_empleado, empleado.nombre_empleado, superior.nombre_empleado as nombre_superior from personal empleado
left join personal superior on superior.id_empleado = empleado.superior_id;


