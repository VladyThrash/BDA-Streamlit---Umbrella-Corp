-- Vladimir Yepez Contreras - S23002520 - IINF.
-- Aquí vamos a colocar los scripts para generar las tablas de la Base de datos 'Umbrella Corp'.


-- Tabla Laboratorio, no aplica llaves foraneas porque es una entidad 1:N con otras entidades relacionadas.
create table Laboratorio (
    codigo_laboratorio varchar(50) PRIMARY KEY NOT NULL,
    nombre_clave VARCHAR(50) NOT NULL,
    metros_profundidad DOUBLE PRECISION
);


-- Tabla Personal con relación uno a muchos recursiva. Llave foranea que relaciona un laboratorio para cada empleado.
create table Personal (
    id_empleado serial PRIMARY KEY,
    nombre_empleado varchar(50) NOT NULL,
    apellido_empleado varchar(50) NOT NULL,
    nivel_autorizacion int CHECK(nivel_autorizacion BETWEEN 1 and 10), -- Este campo se evalúa en tiempo de inserción.
    superior_id int, --Llave forenea recursiva.
    laboratorio_codigo VARCHAR(50), --Llave foranea a laboratorio.
    FOREIGN KEY(superior_id) REFERENCES Personal(id_empleado), -- AQUI DEBDE DE: ON DELETE SET NULL.
    FOREIGN KEY(laboratorio_codigo) REFERENCES Laboratorio(codigo_laboratorio)
);


-- Tabla Zona Brote con catalogo a Estados de Cuarentena.
create table Estado_Cuarentena ( -- Catalogo con los tipos de estados de cuarentena.
    id_estado serial PRIMARY KEY,
    nombre_estado varchar(50) NOT NULL,
    descripcion_estado varchar(200)
);

create table Zona_Brote ( -- Esta entidad implementa el catalogo de estado de cuarentena (es una llave foranea).
    id_geografico INT PRIMARY KEY NOT NULL,
    nombre_zona varchar(50) NOT NULL,
    estado_id INT, -- Llave foranea a el catalogo de estados de cuarentena.
    FOREIGN KEY(estado_id) REFERENCES Estado_Cuarentena(id_estado)
);

ALTER TABLE Zona_Brote  -- Añadir dos nuevas columnas para poder ubicar geograficamente.
ADD COLUMN latitud DOUBLE PRECISION,
ADD COLUMN longitud DOUBLE PRECISION;


-- Tabla Equipo de Contención con catalogo a al tipo de Armamento utilizado.
create table Armamento ( -- Catalogo con los tipos de armamento que puede utilizar un equipo.
    id_armamento serial PRIMARY KEY,
    nombre_armamento varchar(50) NOT NULL,
    descripcion_armamento varchar(200)
);

create table Equipo_Contencion ( -- Esta entidad implementa el catalogo de tipo de armamento 
    codigo_equipo varchar(50) PRIMARY KEY NOT NULL,
    nombre_equipo varchar(50) NOT NULL,
    armamento_id INT, -- Llave foranea al catalogo del tipo de armamento.
    FOREIGN KEY(armamento_id) REFERENCES Armamento(id_armamento)
);


-- Tabla B.O.W y subtablas Humanoides y Zoológicas utilizando llaves foraneas.
-- Tambien se definen los catalogos a utilizar.
create table Cepa_Viral ( -- Catalogo con los tipos de cepa a los que pertenece un B.O.W.
    id_cepa serial PRIMARY KEY,
    nombre_cepa varchar(50) NOT NULL,
    descripcion_cepa varchar(200)
);

create table BOW ( -- Tabla BOW que implementa la llave foranea al laboratorio de creación.
    codigo_lote varchar(50) PRIMARY KEY NOT NULL,
    nombre_clave varchar(50) NOT NULL,
    fecha_mutacion date NOT NULL,
    laboratorio_codigo varchar(50), -- Para la fk con Laboratorio.
    cepa_id INT, -- Para la pk con catalogo cepa.
    FOREIGN KEY(laboratorio_codigo) REFERENCES Laboratorio(codigo_laboratorio),
    FOREIGN KEY(cepa_id) REFERENCES Cepa_Viral(id_cepa)
);

create table Humanoides ( -- Subtabla Humanoides hija de BOW.
    lote_codigo VARCHAR(50) PRIMARY KEY, -- Para la fk con su supertabla.
    valor_iq INT NOT NULL,
    resistencia_daño INT NOT NULL,
    FOREIGN KEY(lote_codigo) REFERENCES BOW(codigo_lote)
);

create table Especie_Animal ( -- Catalogo con especies animales para la subtabla Zoológicas hija de BOW.
    id_especie serial PRIMARY KEY,
    nombre_especie varchar(50) NOT NULL,
    descripcion_especie varchar(200)
);

create table Zoologicas ( -- Subtabla Zoologicas hija de BOW.
    lote_codigo varchar(50) PRIMARY KEY, -- Para la fk con la supertabla.
    tasa_agresividad int NOT NULL,
    especie_id INT, -- Para la fk con el catalogo.
    FOREIGN KEY(lote_codigo) REFERENCES BOW(codigo_lote),
    FOREIGN KEY(especie_id) REFERENCES Especie_Animal(id_especie)
);


-- Tabla Despliegues, es el nodo que más conexiones o llaves foreneas implementa.
-- NUEVA TAREA:
    -- Hacer inmutable esta tabla (permite la adicion pero no permite la eliminación o la modificación de los registros existentes)
create table Despliegues (
    clave_despliegue serial PRIMARY KEY,
    fecha_despliegue date NOT NULL,
    num_especimenes int NOT NULL,
    equipo_codigo varchar(50), -- Para la fk con la tabla Equipo_Contencion.
    geografico_id INT, -- Para la fk con la tabla Zona_Brote.
    empleado_id INT, -- Para la fk con la tabla Personal.
    lote_codigo varchar(50), --Para la fk con la tabla B.O.W.
    FOREIGN KEY(equipo_codigo) REFERENCES Equipo_Contencion(codigo_equipo),
    FOREIGN KEY(geografico_id) REFERENCES Zona_Brote(id_geografico),
    FOREIGN KEY(empleado_id) REFERENCES Personal(id_empleado),
    FOREIGN KEY(lote_codigo) REFERENCES BOW(codigo_lote)
);


-- Tabla Auditoria, la utiliza un trigger para registrar zonas de erradicación o muertas al superar cierto número de especimenes.
-- Solo cuando se sobrepasa el umbral se establece la auditoria.
CREATE TABLE Auditoria (
    fecha_registro date NOT NULL, 
    num_total_especimenes INT, -- Para contabilizar el número total de especimenes de la región.
    geografico_id INT, -- Para la fk con la tabla Zona_Brote.
    FOREIGN KEY(geografico_id) REFERENCES Zona_Brote(id_geografico)
);

-- Tabla de protocolos, cada protocolo se relaciona con un laboratorio (fk).
create table Protocolos (
    num_protocolo serial PRIMARY KEY,
    tiemp_cuenta_regresiva INTERVAL NOT NULL, -- Permite almacenar como cronometro '02:32:20' - Horas:Minutos:Segundos
    cod_activacion_alfa varchar(20) NOT NULL,
    descripcion_protocolo varchar(200),
    laboratorio_codigo varchar(50), -- Para la fk con la tabla Laboratorio.
    FOREIGN KEY(laboratorio_codigo) REFERENCES Laboratorio(codigo_laboratorio) -- AQUI DEBDE: ON DELETE SET NULL
);


-- Tablas para el canal de comunicación de emergencia (envio de mensajes entre Laboratorios).
create table Mensaje ( -- Esta tabla almacena el mensaje y el remitente (fk).
    id_mensaje serial PRIMARY KEY,
    texto_mensaje varchar(1000) NOT NULL,
    laboratorio_org varchar(50), -- Para la fk con la tabla Laboratorio.
    FOREIGN KEY(laboratorio_org) REFERENCES Laboratorio(codigo_laboratorio)
);

CREATE TYPE msg_sys_prior AS ENUM ('ALTA', 'MEDIA', 'BAJA'); -- Tipo ENUM para definir la prioridad de los mensajes.

create table Comunicaciones ( -- Esta tabla almacena la fecha, prioridad, menaje (fk) y destinatario (fk).
    fecha_envio date NOT NULL,
    prioridad msg_sys_prior DEFAULT 'MEDIA', -- Este campo aplica un tipo ENUM.
    mensaje_id INT, -- Para la fk con la tabla Mensaje.
    laboratorio_dest varchar(50), -- Para la fk con la tabla Laboratorio.
    FOREIGN KEY(mensaje_id) REFERENCES Mensaje(id_mensaje),
    FOREIGN KEY(laboratorio_dest) REFERENCES Laboratorio(codigo_laboratorio)
);
