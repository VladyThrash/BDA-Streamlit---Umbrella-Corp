-- Vladimir Yepez Contreras - S23002520 - IINF.
-- Aquí vamos a colocar los scripts que se utilizaran para llenar las tablas y los catalogos.
-- Se inicia con los catalogos para evitar problemas con las llaves foraneas.


-- Para llenar la tabla Laboratorio.
INSERT INTO Laboratorio (codigo_laboratorio, nombre_clave, metros_profundidad) VALUES 
('LAB-ARK-01', 'Instalación de Investigación Arklay', 15.0),
('LAB-NST-01', 'NEST (Raccoon City)', 450.5),
('LAB-NST-02', 'NEST 2', 300.0),
('LAB-ANT-01', 'Base Antártica', 120.75),
('LAB-CAU-01', 'Instalación del Cáucaso', 85.0),
('LAB-PAR-01', 'Laboratorio de París', 25.5);


-- Para llenar la tabla Personal.
-- 1. Nivel Directivo (Las raíces del árbol. No tienen superior y tienen el nivel máximo)
INSERT INTO Personal (id_empleado, nombre_empleado, apellido_empleado, nivel_autorizacion, superior_id, laboratorio_codigo) VALUES 
(1, 'Oswell E.', 'Spencer', 10, NULL, NULL), -- CEO fundador, acceso global
(2, 'Alexander', 'Ashford', 9, NULL, 'LAB-ANT-01'),
(11, 'Sergei', 'Vladimir', 9, 1, 'LAB-CAU-01'), -- Director en el Cáucaso
(12, 'Christine', 'Henry', 8, 1, 'LAB-PAR-01'),   -- Directora del Laboratorio de París
(13, 'Nathaniel', 'Bard', 8, 1, 'LAB-NST-02');    -- Jefe de Investigación en NEST 2

-- 2. Investigadores Principales (Dependen directamente de las raíces)
INSERT INTO Personal (id_empleado, nombre_empleado, apellido_empleado, nivel_autorizacion, superior_id, laboratorio_codigo) VALUES 
(3, 'William', 'Birkin', 8, 1, 'LAB-NST-01'), -- A cargo de NEST, reporta a Spencer
(4, 'Albert', 'Wesker', 8, 1, 'LAB-ARK-01'),  -- En Arklay, reporta a Spencer
(5, 'Alexia', 'Ashford', 8, 2, 'LAB-ANT-01'); -- En la Antártida, reporta a Alexander

-- 3. Jefes de Área y Científicos Senior (Nivel medio)
INSERT INTO Personal (id_empleado, nombre_empleado, apellido_empleado, nivel_autorizacion, superior_id, laboratorio_codigo) VALUES 
(6, 'Annette', 'Birkin', 6, 3, 'LAB-NST-01'), -- Reporta a William
(7, 'John', 'Clemens', 6, 4, 'LAB-ARK-01'),   -- Reporta a Wesker
(14, 'Morpheus D.', 'Duvall', 6, 11, 'LAB-CAU-01'), -- Investigador Senior en Cáucaso
(15, 'Rodrigo Juan', 'Raval', 5, 12, 'LAB-PAR-01'), -- Comandante de Seguridad en París
(16, 'Ryan', 'Howard', 6, 13, 'LAB-NST-02'),        -- Investigador NEST 2
(17, 'Alexander', 'Isaacs', 7, 3, 'LAB-NST-01'),    -- Investigador adjunto a Birkin
(18, 'Carter', 'Burke', 5, 5, 'LAB-ANT-01');        -- Supervisor en la Antártida

-- 4. Personal Operativo y Asistentes (La base del árbol, niveles bajos)
INSERT INTO Personal (id_empleado, nombre_empleado, apellido_empleado, nivel_autorizacion, superior_id, laboratorio_codigo) VALUES 
(8, 'Greg', 'Albright', 3, 6, 'LAB-NST-01'),  -- Asistente en NEST, reporta a Annette
(9, 'Martin', 'Crackhorn', 2, 7, 'LAB-ARK-01'),-- Operativo en Arklay, reporta a John
(10, 'Henry', 'Sarton', 1, 7, 'LAB-ARK-01'),   -- Nivel más bajo, reporta a John
(19, 'Ivan', 'Tyrant', 2, 11, 'LAB-CAU-01'),      -- Escolta personal de Sergei
(20, 'Arthur', 'Gorman', 3, 14, 'LAB-CAU-01'),    -- Técnico de mantenimiento
(21, 'Claire', 'Redfield', 1, 15, 'LAB-PAR-01'),  -- Sujeto de prueba/infiltrada registrada
(22, 'Wayne', 'Lipps', 2, 16, 'LAB-NST-02'),      -- Asistente de laboratorio en NEST 2
(23, 'Edward', 'Dewey', 4, 4, 'LAB-ARK-01'),      -- Piloto y seguridad en Arklay
(24, 'Robert', 'Kendo', 2, 6, 'LAB-NST-01'),      -- Proveedor de equipo registrado
(25, 'Steve', 'Burnside', 1, 18, 'LAB-ANT-01');   -- Prisionero clasificado como operativo bajo


-- Para llenar la tabla Zona_Brote. 
-- Primero con el catalogo Estado_Cuarentena.
INSERT INTO Estado_Cuarentena (id_estado, nombre_estado, descripcion_estado) VALUES 
(1, 'Fase 1: Monitoreo', 'Posible fuga biológica. Observación discreta de la zona sin alterar a la población local ni autoridades.'),
(2, 'Fase 2: Contención Interna', 'Brote confirmado en las instalaciones. Sellado de puertas herméticas y despliegue del equipo USS (Umbrella Security Service).'),
(3, 'Fase 3: Cuarentena Total', 'Infección propagada a nivel urbano. Ley marcial, bloqueo militar de carreteras y restricción de comunicaciones externas.'),
(4, 'Fase 4: Erradicación', 'Pérdida total de control biológico. Aprobación del Código XX: Esterilización mediante ataque con misiles termonucleares.'),
(5, 'Fase 5: Zona Muerta', 'Área post-erradicación. Entorno colapsado, biológicamente inhabitable y con prohibición de acceso gubernamental.');

-- Ahora si procedemos con la tabla.
INSERT INTO Zona_Brote (id_geografico, nombre_zona, estado_id) VALUES 
-- Zonas originales con nombres completos
(101, 'Montañas Arklay', 5),
(102, 'Raccoon City', 5),
(103, 'Isla Sheena', 4),
(104, 'Isla Rockfort', 2),
(105, 'Zona Autónoma de Kijuju', 3),
(106, 'Ciudad de Tall Oaks', 4),
(107, 'Dulvey, Luisiana', 1),
(108, 'Ciudad Flotante Terragrigia', 5), -- Revelations: Erradicada por el satélite Regia Solis
(109, 'República de Edonia', 3),         -- RE6: Zona de guerra con brote del Virus C
(110, 'Lanshiang, China', 4),            -- RE6: Ataque bioterrorista masivo, erradicada
(111, 'Harvardville', 2),                -- Degeneration: Brote contenido en el aeropuerto
(112, 'Isla de Zabytij', 1),             -- Revelations 2: Monitoreo de los experimentos de Alex Wesker
(113, 'Pueblo de Valdelobos, España', 3),-- RE4: Contención militar externa tras la caída de Los Iluminados
(114, 'Villa Europea, Rumania', 2);      -- RE8: Contención interna por las fuerzas de la BSAA

-- Añadir UPDATES para poder rigistrar latitud y longitud (Ubicación geografica).
-- 101: Montañas Arklay (Aproximación Medio Oeste EE.UU.)
UPDATE Zona_Brote SET latitud = 37.9150, longitud = -91.8200 WHERE id_geografico = 101;
-- 102: Raccoon City (Cerca de Arklay)
UPDATE Zona_Brote SET latitud = 37.8020, longitud = -91.9540 WHERE id_geografico = 102;
-- 103: Isla Sheena (Aproximación Europa del Norte)
UPDATE Zona_Brote SET latitud = 54.1230, longitud = 5.0120 WHERE id_geografico = 103;
-- 104: Isla Rockfort (Océano Antártico / Atlántico Sur)
UPDATE Zona_Brote SET latitud = -54.2810, longitud = -36.5050 WHERE id_geografico = 104;
-- 105: Zona Autónoma de Kijuju (África Occidental)
UPDATE Zona_Brote SET latitud = 12.3400, longitud = -3.2100 WHERE id_geografico = 105;
-- 106: Ciudad de Tall Oaks (Costa Este/Medio Oeste EE.UU.)
UPDATE Zona_Brote SET latitud = 40.1200, longitud = -77.0300 WHERE id_geografico = 106;
-- 107: Dulvey, Luisiana (Pantanos del sur de EE.UU.)
UPDATE Zona_Brote SET latitud = 29.9510, longitud = -90.8710 WHERE id_geografico = 107;
-- 108: Ciudad Flotante Terragrigia (Mar Mediterráneo, cerca de Italia)
UPDATE Zona_Brote SET latitud = 42.1050, longitud = 12.2130 WHERE id_geografico = 108;
-- 109: República de Edonia (Europa del Este, Balcanes)
UPDATE Zona_Brote SET latitud = 44.2100, longitud = 21.0500 WHERE id_geografico = 109;
-- 110: Lanshiang, China (Inspirado en la costa este asiática)
UPDATE Zona_Brote SET latitud = 22.3193, longitud = 114.1694 WHERE id_geografico = 110;
-- 111: Harvardville (EE.UU.)
UPDATE Zona_Brote SET latitud = 39.0520, longitud = -94.3410 WHERE id_geografico = 111;
-- 112: Isla de Zabytij (Mar Báltico/Rusia)
UPDATE Zona_Brote SET latitud = 60.1500, longitud = 28.1200 WHERE id_geografico = 112;
-- 113: Pueblo de Valdelobos, España (Norte de España)
UPDATE Zona_Brote SET latitud = 43.1500, longitud = -5.3200 WHERE id_geografico = 113;
-- 114: Villa Europea, Rumania (Transilvania)
UPDATE Zona_Brote SET latitud = 46.1200, longitud = 24.3500 WHERE id_geografico = 114;


-- Para llenar la tabla Equipo_Contención.
-- Primero llenamos el catalogo de Armamento.
INSERT INTO Armamento (id_armamento, nombre_armamento, descripcion_armamento) VALUES 
(1, 'Beretta M92F Custom (Samurai Edge)', 'Pistola táctica de 9mm modificada. Alta precisión y fiabilidad como arma secundaria.'),
(2, 'Rifle de Asalto CQBR', 'Arma automática de dotación estándar para la USS. Alta cadencia para control de masas infecciosas.'),
(3, 'Escopeta Remington M870', 'Arma de corredera letal a corta distancia. Ideal para detener el avance de bioarmas estándar.'),
(4, 'Lanzagranadas M79', 'Soporta munición explosiva, incendiaria y de ácido. Esencial contra mutaciones avanzadas del Virus-G.'),
(5, 'Lanzallamas Químico', 'Dispersor alimentado por napalm modificado. Diseñado para purgar mutaciones basadas en flora (Ej. Planta 42).'),
(6, 'Lanzacohetes Anti-Tanque (AT4)', 'Fuego pesado de un solo uso. Autorizado exclusivamente para neutralización de bioarmas clase Tyrant.'),
(7, 'Arma de Partículas (P.R.L. 412)', 'Armamento experimental de energía. Penetra blindajes biológicos y erradica parásitos a nivel celular.');

-- Ya podemos proceder con la tabla principal.
INSERT INTO Equipo_Contencion (codigo_equipo, nombre_equipo, armamento_id) VALUES 
('USS-ALP', 'U.S.S. Equipo Alpha', 2),    -- Liderados por HUNK, asalto estándar
('USS-DEL', 'U.S.S. Equipo Delta', 4),    -- Unidad de soporte con artillería pesada
('UBCS-A', 'U.B.C.S. Pelotón Alfa', 2),   -- Mercenarios de contención masiva
('UBCS-D', 'U.B.C.S. Pelotón Delta', 3),  -- Especialistas en interiores y rescate
('PURG-1', 'Unidad de Incineración', 5),  -- Asignados al control de biomasa y flora
('NEM-T02', 'Persecutor Némesis', 6),     -- Despliegue especial anti-Tyrant
('STARS-A', 'S.T.A.R.S. Equipo Alpha', 1);-- Equipo táctico local con armas de precisión


-- Para la tabla B.O.W. y sus subtablas (ISA).
-- Primero el catalogo que implementa la supertabla (Cepa_Viral).
INSERT INTO Cepa_Viral (id_cepa, nombre_cepa, descripcion_cepa) VALUES 
(1, 'Virus Progenitor', 'Cepa madre original descubierta en la flor Sonnentreppe. Altamente letal, sirve como base para todas las investigaciones de Umbrella.'),
(2, 'Virus T (Tyrant)', 'Diseñado para crear soldados bio-orgánicos. Causa necrosis severa, reanimación de tejido muerto y canibalismo agresivo.'),
(3, 'Virus G (Golgotha)', 'Otorga regeneración celular acelerada y mutaciones impredecibles. El huésped evoluciona constantemente para adaptarse al daño.'),
(4, 'Virus T-Veronica', 'Integra ADN de hormiga reina y plantas. Permite conservar la inteligencia y controlar masas si se incuba criogénicamente.'),
(5, 'Las Plagas', 'Parásitos fosilizados que asimilan el sistema nervioso central, permitiendo control mental sobre el huésped sin pudrir la carne.'),
(6, 'Uroboros', 'Fuerza la selección natural biológica. Si el ADN es incompatible, consume al huésped transformándolo en una masa de pústulas negras.'),
(7, 'Virus C (Chrysalid)', 'Combina atributos del T-Veronica y el G. Permite conservar el uso de armas y tácticas antes de mutar mediante un estado de crisálida.');

-- Supertabla BOW.
INSERT INTO BOW (codigo_lote, nombre_clave, fecha_mutacion, laboratorio_codigo, cepa_id) VALUES 
('BOW-T002', 'Tyrant T-002', '1998-07-24', 'LAB-ARK-01', 2),          -- Creado en Arklay con Virus T
('BOW-MA121', 'Hunter Alpha', '1998-05-11', 'LAB-ARK-01', 2),         -- Investigaciones previas en Arklay
('BOW-G001', 'William Birkin (G-Mutant)', '1998-09-22', 'LAB-NST-01', 3), -- Mutación en NEST con Virus G
('BOW-LK001', 'Licker', '1998-09-24', 'LAB-NST-01', 2),               -- Mutación secundaria en Raccoon (NEST)
('BOW-T103', 'Tyrant T-103 (Mr. X)', '1998-09-25', 'LAB-CAU-01', 2),  -- Producción en masa en el Cáucaso
('BOW-NEM01', 'Nemesis-T Type', '1998-09-28', 'LAB-PAR-01', 2),       -- Desarrollado por Umbrella Europa (París)
('BOW-TV001', 'Alexia Ashford', '1998-12-27', 'LAB-ANT-01', 4),       -- Despertar criogénico en la Antártida
('EXP-LST', 'Lisa Trevor', '1967-11-10', 'LAB-ARK-01', 1),            -- Expuesta al Progenitor original y probada durante décadas
('HTR-A', 'Hunter Beta', '1998-05-15', 'LAB-ARK-01', 2),             -- BOW reptiliano base creado en la Mansión Spencer
('T-103', 'Tyrant T-104 (Mr. Y)', '1998-09-01', 'LAB-NST-01', 2),     -- Producción en masa de Tyrants en instalaciones de Raccoon
('LICK-01', 'Licker (Mutante Irregular)', '1998-09-24', 'LAB-NST-01', 2), -- Mutación secundaria de zombis por el Virus T
('HTR-G', 'Hunter Gamma', '1998-09-26', 'LAB-NST-02', 2),             -- Variante anfibia probada en NEST 2
('BND-01', 'Bandersnatch', '1998-12-15', 'LAB-ANT-01', 2),            -- Variante de Tyrant económico y defectuoso
('ALX-01', 'Nosferatu (Alexander Ashford)', '1983-03-03', 'LAB-ANT-01', 4), -- Mutación fallida del T-Veronica encadenado en la Antártida
('STV-01', 'Steve Burnside (Mutado)', '1998-12-27', 'LAB-ANT-01', 4), -- Infección forzada para probar la viabilidad del T-Veronica
('G-02', 'G-Birkin (Fase 2)', '1998-09-29', 'LAB-NST-01', 3),         -- Evolución asimétrica por daño extremo
('PLG-GG', 'El Gigante', '2004-10-15', 'LAB-CAU-01', 5),              -- Modificación de Las Plagas transferida a instalaciones rusas
('URB-MK', 'Uroboros Mkono', '2009-03-07', 'LAB-CAU-01', 6),          -- Consumo total del huésped por incompatibilidad genética
('JV-01', 'J''avo', '2012-12-24', 'LAB-CAU-01', 7);                   -- Infección de mercenarios con el Virus C

-- Subtabla Humanoides (No requiere un catalogo).
INSERT INTO Humanoides (lote_codigo, valor_iq, resistencia_daño) VALUES 
('BOW-T002', 65, 80),    -- Tyrant T-002: Inteligencia básica para acatar órdenes simples. Alta resistencia.
('BOW-T103', 75, 90),    -- Mr. X (T-103): Comprensión táctica moderada (abrir puertas, rastrear). Resistencia superior por su capa limitadora.
('BOW-NEM01', 115, 98),  -- Nemesis-T Type: Alta inteligencia gracias al parásito NE-Alpha (usa lanzacohetes y rastrea). Resistencia extrema.
('BOW-TV001', 180, 85),  -- Alexia Ashford: Conserva su intelecto humano de nivel genio tras la criogenización.
('EXP-LST', 35, 100),    -- Lisa Trevor: Capacidad cognitiva severamente degradada, pero regeneración que la hace virtualmente inmortal.
('T-103', 75, 90),       -- Mr. Y (Variante de producción T-104): Mismos stats base que Mr. X.
('BND-01', 50, 70),      -- Bandersnatch: Variante de Tyrant económica y defectuosa. Menor comprensión y resistencia física.
('ALX-01', 40, 75),      -- Nosferatu: Enloquecido por años de confinamiento, actúa por instinto agresivo.
('STV-01', 60, 85),      -- Steve Burnside: Bestializado, pero logra retener destellos de memoria humana al final.
('BOW-G001', 55, 80),    -- William Birkin (G1): Aún balbucea palabras humanas, impulsado por instinto de reproducción.
('G-02', 35, 85),        -- G-Birkin (Fase 2): Pierde casi toda su consciencia original, se vuelve más resistente al daño balístico.
('PLG-GG', 30, 95),      -- El Gigante: Capacidad intelectual nula (ataca a sus aliados), pero requiere fuego pesado para caer.
('JV-01', 100, 60);      -- J'avo: Inteligencia táctica humana (coordinan ataques, conducen tanques), resistencia moderada antes de mutar.

-- Catalogo que define la Especie Animal sobre la que se trabajo la mutación.
INSERT INTO Especie_Animal (id_especie, nombre_especie, descripcion_especie) VALUES 
(1, 'Reptil', 'Mutaciones basadas en lagartos y otros reptiles. Alta velocidad y garras afiladas.'),
(2, 'Anfibio', 'ADN de ranas y sapos. Requieren ambientes húmedos y suelen carecer de visión ocular.'),
(3, 'Mamífero Primate', 'Sujetos de origen homínido (humanos o simios) con regresión bestial extrema.'),
(4, 'Canino', 'Perros de presa u otros cánidos infectados. Altamente territoriales.'),
(5, 'Anélido / Sanguijuela', 'Organismos formados por colonias de gusanos parasitarios o sanguijuelas.');

-- Subtabla Zoologicas, implementa el catalogo anterior.
INSERT INTO Zoologicas (lote_codigo, tasa_agresividad, especie_id) VALUES 
('BOW-MA121', 95, 1), -- Hunter Alpha: Instinto asesino alto, ADN de reptil.
('HTR-A', 90, 1),     -- Hunter Beta: Mejora del Alpha, agresividad ligeramente ajustada para obedecer.
('HTR-G', 85, 2),     -- Hunter Gamma: Anfibio, letal pero su agresividad depende más de su entorno húmedo.
('BOW-LK001', 100, 3),-- Licker: Depredador ciego impulsado por el sonido. Hostilidad total al detectar presas.
('LICK-01', 100, 3),  -- Licker (Mutante Irregular): Hostilidad descontrolada igual que el anterior.
('URB-MK', 98, 5);    -- Uroboros Mkono: Aunque el huésped era humano, es consumido totalmente por anélidos (sanguijuelas).


-- Para la tabla transaccional Despliegues.
INSERT INTO Despliegues (fecha_despliegue, num_especimenes, equipo_codigo, geografico_id, empleado_id, lote_codigo) VALUES 
-- 1. Incidente de la Mansión: Albert Wesker (4) despliega al Tyrant contra el equipo S.T.A.R.S. en Arklay.
('1998-07-24', 1, 'STARS-A', 101, 4, 'BOW-T002'), 
-- 2. Extracción de NEST: La U.S.S. Alpha acorrala a William Birkin (3) en Raccoon City, provocando que se inyecte el Virus G.
('1998-09-22', 1, 'USS-ALP', 102, 3, 'BOW-G001'), 
-- 3. Despliegue de Némesis: Christine Henry (12) autoriza desde París lanzar a Némesis en Raccoon City.
('1998-09-28', 1, 'NEM-T02', 102, 12, 'BOW-NEM01'), 
-- 4. Operación Raccoon City: Sergei Vladimir (11) lanza múltiples Tyrants en masa, cruzándose con la U.B.C.S.
('1998-09-29', 6, 'UBCS-A', 102, 11, 'BOW-T103'), 
-- 5. Incidente de Rockfort: Alexander Ashford (2) (o su linaje) lidia con el brote donde se usan Bandersnatches contra la USS Delta.
('1998-12-27', 15, 'USS-DEL', 104, 2, 'BND-01'),
-- 6. Pruebas de campo Arklay: John Clemens (7) coordina pruebas de descarte de Hunters junto con unidades de incineración.
('1998-05-15', 5, 'PURG-1', 101, 7, 'HTR-A'),
-- 7. Contención en el Cáucaso: Sergei Vladimir (11) usa a la U.B.C.S. Delta para probar a los T-103 en su instalación de Rusia.
('2003-02-18', 3, 'UBCS-D', 111, 11, 'BOW-T103');


-- Definición de Protocolos para los Laboratorios.
INSERT INTO Protocolos (tiemp_cuenta_regresiva, cod_activacion_alfa, descripcion_protocolo, laboratorio_codigo) VALUES 
('00:03:00', 'JOHN-ADA-98', 'Autodestrucción de las instalaciones y purga térmica de especímenes escapados.', 'LAB-ARK-01'),
('00:10:00', 'G-PURGE-124', 'Desbloqueo de tren de escape subterráneo y detonación del reactor principal.', 'LAB-NST-01'),
('00:15:00', 'VAC-N2-88', 'Bloqueo hermético de cámaras de cultivo y despliegue del arma de riel Ferromagnetic.', 'LAB-NST-02'),
('00:12:30', 'ALX-VER-1998', 'Activación del sistema de autodestrucción y liberación del Linear Launcher.', 'LAB-ANT-01'),
('00:08:45', 'TALOS-RED-00', 'Borrado de matriz de datos U.M.F.-013 y colapso estructural de la base.', 'LAB-CAU-01'),
('00:05:00', 'NEMESIS-T-DEL', 'Incineración de laboratorios de prueba de parásitos NE-Alpha y borrado de servidores.', 'LAB-PAR-01'),
('00:05:00', 'CHEM-PURGE-98', 'Inyección de químicos corrosivos en los ductos de ventilación del ala de invitados.', 'LAB-ARK-01'),
('00:02:30', 'VJOLT-FAILSAFE', 'Cierre hermético del invernadero e inundación del sistema de riego con compuesto V-JOLT.', 'LAB-ARK-01'),
('00:08:00', 'CRIO-LOCK-A1', 'Congelación relámpago a -100°C del ala de contención para detener la actividad celular del Virus G.', 'LAB-NST-01'),
('00:15:00', 'R-QUEEN-SHUT', 'Desconexión física del mainframe de la IA y sellado de titanio en el cuarto central de servidores.', 'LAB-NST-01'),
('00:12:00', 'BIO-DRAIN-77', 'Drenaje rápido de fluidos de incubación y esterilización térmica de las cápsulas cilíndricas.', 'LAB-NST-02'),
('01:00:00', 'VERONICA-CRIO', 'Apagado del soporte vital general y transición de la base a un estado de criostasis profunda de 15 años.', 'LAB-ANT-01'),
('00:05:45', 'POD-EJECT-00', 'Expulsión de emergencia de cápsulas de escape submarinas e inundación de hangares.', 'LAB-ANT-01'),
('00:04:15', 'EMP-CAUCASUS', 'Sobrecarga del generador central para emitir un pulso electromagnético masivo (Borrado T.A.L.O.S.).', 'LAB-CAU-01'),
('00:07:30', 'NERVE-GAS-X', 'Inyección de gas nervioso letal en el ala de prisioneros para evitar fugas de sujetos de prueba.', 'LAB-PAR-01');


-- Sistema de Comunicación, mensajes de cardinalidad (1:1 y 1:N).
-- El mensaje es un ente aislado de la comunicación efectuada.
INSERT INTO Mensaje (texto_mensaje, laboratorio_org) VALUES 
('Brecha de contención confirmada en los niveles inferiores. Tasa de infección del 90%. El personal se ha transformado. Solicito extracción de los investigadores principales.', 'LAB-ARK-01'), -- ID 1 (Incidente Arklay)
('El Virus G es mi creación absoluta. Me niego rotundamente a entregar las muestras maestras a la junta directiva. He contactado al ejército estadounidense.', 'LAB-NST-01'), -- ID 2 (Rebelión de Birkin)
('El proyecto T-Veronica ha entrado en fase de criostasis. Tiempo estimado para la adaptación celular simbiótica: 15 años. Iniciar monitoreo automatizado.', 'LAB-ANT-01'), -- ID 3 (Diarios de la Antártida)
('Orden ejecutiva de la sede: Interceptar a Birkin antes de que logre su trato con los militares y asegurar la muestra del Virus G. Escuadrón U.S.S. Alpha desplegado.', 'LAB-PAR-01'); -- ID 4 (Órdenes de París)

-- Inserción de Comunicaciones (La tabla pivote transaccional).
INSERT INTO Comunicaciones (fecha_envio, prioridad, mensaje_id, laboratorio_dest) VALUES 
-- COMUNICACIÓN UNO A UNO
-- Arklay avisa a NEST (Raccoon City) de la catástrofe de las sanguijuelas / fugas iniciales.
('1998-05-11', 'ALTA', 1, 'LAB-NST-01'),
-- COMUNICACIÓN UNO A MUCHOS
-- Birkin (NEST) desafiando a los directivos en Europa y Rusia de manera simultánea.
('1998-09-15', 'ALTA', 2, 'LAB-PAR-01'),
('1998-09-15', 'MEDIA', 2, 'LAB-CAU-01'),
-- COMUNICACIÓN UNO A UNO
-- Reporte histórico de Alexander Ashford desde la Antártida hacia las instalaciones fundadoras de Arklay.
('1983-12-31', 'BAJA', 3, 'LAB-ARK-01'),
-- COMUNICACIÓN UNO A MUCHOS
-- París ordena la cuarentena y extracción a toda la red de laboratorios NEST en Raccoon City.
('1998-09-20', 'ALTA', 4, 'LAB-NST-01'),
('1998-09-20', 'ALTA', 4, 'LAB-NST-02');
