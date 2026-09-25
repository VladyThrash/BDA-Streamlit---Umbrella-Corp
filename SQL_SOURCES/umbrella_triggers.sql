-- Vladimir Yepez Contreras - S23002520 - IINF.
-- Aquí vamos a colocar los scripts para triggers de validación y auditoría.


CREATE OR REPLACE FUNCTION limitar_num_especimenes() -- Primero definimos la función que ejecutara el trigger.
RETURNS TRIGGER AS $$
BEGIN
    IF new.num_especimenes > 20 THEN -- Anclamos el número de especimenes a 20.
        new.num_especimenes := 20;
    END IF;
    RETURN new; -- Devolvemos el dato al flujo de inserción.
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_control_despliegue -- Ahora definimos el trigger y el contexto en el que ejecuta la función.
before INSERT OR UPDATE on Despliegues
FOR each ROW
EXECUTE FUNCTION limitar_num_especimenes();


-- Trigger para validar que los metros de profundidad de un laboratorio sean mas que 0m.
CREATE OR REPLACE FUNCTION limitar_mtr_profundidad()
returns TRIGGER AS $$
BEGIN
    IF new.metros_profundidad < 0 THEN
        new.metros_profundidad := 0;
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_control_laboratorio
before INSERT OR UPDATE ON Laboratorio
FOR each ROW
EXECUTE FUNCTION limitar_mtr_profundidad();


-- Validar que solo los científicos con nivel de autorización 8 puedan autorizar 
-- especímenes de clasificación Nemesis o Tyrant.
CREATE OR REPLACE FUNCTION validar_nivel_autorizacion()
RETURNS TRIGGER AS $$
BEGIN
    IF ((SELECT nivel_autorizacion FROM Personal WHERE id_empleado = new.empleado_id) < 8 ) AND 
        (SELECT nombre_clave ~* 'Tyrant|Nemesis' FROM BOW WHERE codigo_lote = new.lote_codigo) THEN
        RAISE EXCEPTION 'ALERTA DE SEGURIDAD: Autorización insuficiente. Se requiere nivel 8 o superior para este despliegues tipo Nemesis o Tyrant.';
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_control_nivel
BEFORE INSERT OR UPDATE ON Despliegues
FOR each ROW
EXECUTE FUNCTION validar_nivel_autorizacion();


-- Disparar un trigger BEFORE/AFTER INSERT en la tabla de despliegues: si el 
-- número acumulado de especímenes en una zona supera el umbral crítico (ej. > 50), 
-- el estado de la zona debe actualizarse automáticamente a Cuarentena Nivel 4 y 
-- generar un registro en una tabla de auditoría/incidentes.
CREATE OR REPLACE FUNCTION validar_numero_especimenes()
RETURNS TRIGGER AS $$
DECLARE
    total_esp INT; -- Variables a utilizar en la función.
BEGIN
    total_esp := (SELECT sum(num_especimenes) FROM despliegues where geografico_id = new.geografico_id) + new.num_especimenes;
    IF total_esp >= 50 THEN
        IF total_esp < 100 THEN
            -- Update a cuarentena nivel 4 (Erradicación).
            UPDATE Zona_Brote
            SET estado_id = 4
            WHERE id_geografico = new.geografico_id;
        ELSE
            -- Update a cuarentena nivel 5 (Zona muerta).
            UPDATE Zona_Brote
            SET estado_id = 5
            WHERE id_geografico = new.geografico_id;
        END IF;
        -- Insersión a tabla Auditoría.
        INSERT INTO Auditoria(fecha_registro, num_total_especimenes, geografico_id)
        VALUES
            (CURRENT_DATE, total_esp, new.geografico_id);
    END IF;
    return new;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_control_especimenes
BEFORE INSERT OR UPDATE ON Despliegues
FOR EACH ROW
EXECUTE FUNCTION validar_numero_especimenes();


-- Evitar alteraciones o eliminaciones históricas de despliegues pasados 
-- (inmutabilidad de eventos biológicos).
CREATE OR REPLACE FUNCTION aplicar_inmutabilidad()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'REGISTROS INMUTABLES EN TABLA DESPLIEGUES.';
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_control_inmutabilidad
BEFORE UPDATE OR DELETE ON Despliegues
FOR EACH ROW
EXECUTE FUNCTION aplicar_inmutabilidad();

