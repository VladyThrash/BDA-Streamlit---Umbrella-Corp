# ** BDA Streamlit - Umbrella Corp **

Sistema de gestión, base de datos e interfaz gráfica para las operaciones de Umbrella Corp.

## ** Estructura del Proyecto **

### ** PYTHON_FUNC **
Dentro de esta carpeta se encuentra el núcleo de la aplicación web, dividido de la siguiente manera:

** UmbrellaCorp_FP.py (FRONT PANEL) **
Es la interfaz gráfica con la que interactuarán nuestros científicos (Vista del usuario). Implementará las funciones y clases encargadas de la conexión a la base de datos y la lógica del negocio.

** UmbrellaCorp_DBM.py (DATA BASE MANAGER) **
Es la clase encargada del manejo de la conexión a la base de datos PostgreSQL (consultas, inserciones, transacciones, cifrado, etc.). Su función solo obedece al trabajo en "crudo" de los datos. 
Cada uno de los métodos mapea perfectamente una tabla, por lo que podemos utilizar, por ejemplo, `DBM.getPersonal()` para obtener los registros de dicha tabla. Además, podemos seleccionar qué campos no queremos traer en función de la desactivación de los parámetros "default".

** UmbrellaCorp_BL.py (BUSINESS LOGIC) **
Se encarga del procesamiento de los datos en función a la lógica de negocio de Umbrella. Permitirá procesar información tanto para su presentación en el FRONT PANEL como para su almacenamiento a través del DATA BASE MANAGER.

** Objetos Containers (Contenedores) **
Se definen objetos *containers* para almacenar registros específicos. Por ejemplo, un registro de usuario que tiene los campos `id`, `nombre`, `apellido`. Su funcionalidad es envolver todos estos campos sin tener que trabajar con estructuras de datos genéricas como listas o diccionarios. Deben pensarse como tipos STRUCTS.

### ** SQL_SOURCES **
Esta carpeta contiene todos los *scripts* necesarios para estructurar, inicializar y mantener la base de datos relacional de la corporación (PostgreSQL). Incluye:

** umbrella_tables.sql **
Definición de las tablas, jerarquías de claves foráneas y el esquema relacional principal.

** umbrella_insertions.sql **
Inserción de los registros y datos iniciales para la operación del sistema.

** umbrella_querys.sql **
Consultas principales e interacciones recurrentes utilizadas por el Data Base Manager.

** umbrella_stored_procedures.sql **
Procedimientos almacenados para manejar transacciones complejas, asegurando la integridad de los datos mediante *rollbacks* en caso de fallos.

** umbrella_triggers.sql **
Disparadores en PL/pgSQL para la validación de registros y la automatización de respuestas (como protocolos de respuesta ante amenazas).

** umbrella_cte.sql **
Consultas recursivas (Common Table Expressions) diseñadas para navegar por las estructuras jerárquicas complejas de la organización.
