-- Vladimir Yepez Contreras - IINF - S23002520.

-- Diseñar un Stored Procedure transaccional para el alta de un despliegue con 
-- manejo de errores (ROLLBACK automático si falla la asignación de armamento al 
-- escuadrón o si el personal asignado no cumple los permisos mínimos)

CREATE OR REPLACE PROCEDURE nuevo_despliegue(num_especimenes_sp INT, equipo_codigo_sp varchar, geografico_id_sp INT, empleado_id_sp INT, lote_codigo_sp varchar)
LANGUAGE plpgsql
AS $$
DECLARE
    estado_escuadron VARCHAR;
    estado_personal INT;
BEGIN
    estado_escuadron := (SELECT codigo_equipo FROM Equipo_Contencion WHERE armamento_id IS NOT NULL AND codigo_equipo = equipo_codigo_sp);
    estado_personal := (SELECT nivel_autorizacion FROM Personal WHERE id_empleado = empleado_id_sp);

    INSERT INTO Despliegues(fecha_despliegue, num_especimenes, equipo_codigo, geografico_id, empleado_id, lote_codigo)
    VALUES
        (CURRENT_DATE, num_especimenes_sp, equipo_codigo_sp, geografico_id_sp, empleado_id_sp, lote_codigo_sp);

    IF estado_escuadron IS NULL OR estado_personal < 7 THEN
        ROLLBACK; -- Deshacemos el INSERT.
        RAISE NOTICE 'La asignación de ESCUADRON o PERSONAL ha fallado para DESPLIEGUES. Retornando al estado anterior.';
        RETURN; -- Salir de procedure.
    END IF;

    COMMIT;-- COMMIT PARA VALIDAR LOS CAMBIOS.

END;
$$;