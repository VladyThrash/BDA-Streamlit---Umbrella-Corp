# Vladimir Yepez Contreras - S23002520 - IINF.

#Estructura:
#   - UmbrellaCorp_FP.py (FRONT PANEL) es la interfaz gráfica con la que interactuaran nuestros científicos (Vista del usuario), 
#     implementara las funciones y clases encargadas de la conexión a la BD y la lógica del negocio.
#   - UmbrellaCorp_DBM.py (DATA BASE MANAGER) es la encargada del manejo de la conexión a la BD (consultas, insersiones, transacciones, 
#     cifrado, etc). Su función solo obedece al trabajo en "crudo" de los datos de esta BD en concreto.
#   - UmbrellaCorp_BL.py (BUSINESS LOGIC) se encarga del procesamiento de los datos en función a la lógica de negocio de Umbrella.
#     Permitira procesar información tanto para presentación (FRONT PANEL) como para almacenamiento (DATA BASE MANAGER).


#Importamos las librerías y clases necesarias para este módulo.
import psycopg2
from psycopg2 import pool, Error


#Creamos la clase DBM (DATA BASE MANAGER), los métodos estan tipificados concretamente para la base de datos de Umbrella.
#Cada uno de los métodos mapea perfectamente una tabla, por lo que podemos utilizar, por ejemplo, DBM.getPersonal() para obtener los
#registros de dicha tabla. Ademas podemos selecionar que campos no queremos traer en función de la desactivación de los parametros "default".
class DBM:

    #Constructor de la clase. Crea la conexión con la BD (necesita las credenciales) y genera el pool para las consultas de los métodos
    #get y push (getconn). Además nos permite generar multiples instancias o conexiones a la BD.
    def __init__(self, host:str = None, database:str = None, user:str = None, password:str = None, port:str = None):
        #Conectarse con una base de datos existente y generar el pool de conexiones.
        try:
            #El pool es un atributo de la instancia.
            self.pool = psycopg2.pool.ThreadedConnectionPool( #Threaded permite generar varias instancias (usuarios) usando hilos.
                minconn= 1,  #Mínimo de conexiones.
                maxconn= 10, #Máximo de conexiones.
                host= host,
                database= database,
                user= user,
                password= password,
                port= port
            )
            
            if self.pool:
                print("Pool de conexiones a PostgreSQL creado exitosamente")
                
        except Error as e:
            print(f"Error al crear el pool en PostgreSQL: {e}")
            self.pool = None


    #Obtenemos los registros de la tabla "Personal".
    def getPersonal(self, id_empleado:bool = True, nombre_empleado:bool = True, apellido_empleado:bool = True, nivel_autorizacion:bool = True, superior_id:bool = True, laboratorio_codigo:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "personal")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Armamento".
    def getArmamento(self, id_armamento:bool = True, nombre_armamento:bool = True, descripcion_armamento:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "armamento")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "BOW".
    def getBOW(self, codigo_lote:bool = True, nombre_clave:bool = True, fecha_mutacion:bool = True, laboratorio_codigo:bool = True, cepa_id:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "bow")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Cepa_Viral".
    def getCepaViral(self, id_cepa:bool = True, nombre_cepa:bool = True, descripcion_cepa:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "cepa_viral")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Comunicaciones".
    def getComunicaciones(self, fecha_envio:bool = True, prioridad:bool = True, mensaje_id:bool = True, laboratorio_dest:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "comunicaciones")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Despliegues".
    def getDespliegue(self, clave_despliegue:bool = True, fecha_despliegue:bool = True, num_especimenes:bool = True, equipo_codigo:bool = True, geografico_id:bool = True, empleado_id:bool = True, lote_codigo:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "despliegue")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Equipo_Contencion".
    def getEquipoContencion(self, codigo_equipo:bool = True, nombre_equipo:bool = True, armamento_id:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "equipo_contencion")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Especie_Animal".
    def getEspecieAnimal(self, id_especie:bool = True, nombre_especie:bool = True, descripcion_especie:bool =True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "especie_animal")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Estadoo_Cuarentena".
    def getEstadoCuarentena(self, id_estado:bool = True, nombre_estado:bool = True, descripcion_estado:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "estado_cuarentena")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Humanoides".
    def getHumanoides(self, valor_iq:bool = True, resistencia_daño:bool = True, lote_codigo:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "humanoides")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Laboratorio".
    def getLaboratorio(self, codigo_laboratorio:bool = True, nombre_clave:bool = True, metros_profundidad:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "laboratorio")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Mensaje".
    def getMensaje(self, id_mensaje:bool = True, laboratorio_org:bool = True, texto_mensaje:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "mensaje")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Protocolos".
    def getProtocolos(self, num_protocolo:bool = True, tiemp_cuent_regresiva:bool = True, cod_activacion_alfa:bool = True, descripcion_protocolo:bool = True, laboratorio_codigo:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "protocolos")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Zona_Brote".
    def getZonaBrote(self, id_geografico:bool = True, nombre_zona:bool = True, estado_id:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "zona_brote")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Zoologicas".
    def getZoologicas(self, tasa_agresividad:bool = True, lote_codigo:bool = True, especie_id:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "zoologicas")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado.


    #Obtenemos todos los registros de la tabla "Auditoría".
    def getAuditoria(self, fecha_registro:bool = True, numero_total_especimenes:bool = True, geografico_id:bool = True):
        #Generamos un diccionario con todos los parametros de entrada.
        params = locals()
        params.pop('self', None) #Eliminamos el self del diccionario.

        #Obtenemos el query
        query = DBM.parseQuery(params, "auditoria")
        return self.executeSelectFromPool(query) #Ejecutamos el query parseado. 


    #Ejecutamos un SELECT dada una consulta parseada previamente, tomando un hilo del Pool de conexiones.
    def executeSelectFromPool(self, query:str):
        #Obtenemos una conexión del pool.
        conexion = self.pool.getconn()

        #Hacemos la consulta.
        print(query)
        try:
            cur = conexion.cursor()
            cur.execute(query)
            resultados = cur.fetchall()
            cur.close()
            return resultados

        #Si falla retornamos None.  
        except Error as e:
            print(f"Error en la consulta: {e}")
            return None

        #Devolvemos la conexión al pool.
        finally:
            if conexion:
                self.pool.putconn(conexion)


    #Ejecutar consultas que modifican la base de datos (INSERT, UPDATE, DELETE, PROCEDURES), tomando un hilo del Pool de conexiones.
    def executeModifyFromPool(self, query:str, autocommit:bool=False)->str:
        #Obtenemos una conexión del pool.
        conexion = self.pool.getconn()
        
        #Hacemos la consulta.
        print(query)
        try:
            if autocommit:  #Desactivar BEGIN implícito (Se lo dejamos al SP).
                conexion.autocommit = True

            cur = conexion.cursor()
            cur.execute(query)

            if autocommit is not True:
                conexion.commit() #Confirmar la transacción para que los cambios se apliquen permanentemente.
            
            #Manejo inteligente de retornos (ej. INSERT ... RETURNING id).
            #resultados = None
            #if cur.description:  # Verifica si la consulta arrojó datos de vuelta
            #    resultados = cur.fetchall()   
            cur.close()
            
            # Retornamos los datos si hubo un RETURNING, o True si solo fue una ejecución exitosa.
            return "QUERY SUCCESS"

        #Si falla, revertimos y retornamos el error.  
        except Error as e:
            print(f"Error en la ejecución: {e}")
            #Deshacer los cambios para limpiar la transacción fallida.
            if autocommit is not True:
                conexion.rollback()
            return f"ERROR: {e}"

        #Devolvemos la conexión al pool.
        finally:
            if conexion:
                conexion.autocommit = False #Reconfigurar conexion.
                self.pool.putconn(conexion)


    #Métodos estáticos de utileria.


    #Parsear la consulta CTE recursiva.
    @staticmethod
    def parseCTEQuery(id_empleado:int):
        part1 = """
            WITH RECURSIVE cadena_mando as (
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
                id_empleado = 
        """
        part2 = """
            UNION ALL
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
        """
        return part1 + str(id_empleado) + part2 # El ID es la raiz de la jerarquia.


    #Parsear los parametros para las consultas
    @staticmethod
    def parseQuery(params:dict, table:str = None):
        if table is None: #No se especificó la tabla, no se puede realizar la consulta.
            return None

        #Aquí las llamadas para cada tabla
        query = str()
        if table.lower() == "personal":
            query = DBM.parsePersonal(params)
        if table.lower() == "armamento":
            query = DBM.parseArmemento(params)
        if table.lower() == "bow":
            query = DBM.parseBow(params)
        if table.lower() == "cepa_viral":
            query = DBM.parserCepaViral(params)
        if table.lower() == "comunicaciones":
            query = DBM.parseComunicaciones(params)
        if table.lower() == "despliegues":
            query = DBM.parseDespliegues(params)
        if table.lower() == "equipo_contencion":
            query = DBM.parseEquipoContencion(params)
        if table.lower() == "especie_animal":
            query = DBM.parseEspecieAnimal(params)
        if table.lower() == "estado_cuarentena":
            query = DBM.parseEstadoCuarentena(params)
        if table.lower() == "humanoides":
            query = DBM.parseHumanoides(params)
        if table.lower() == "laboratorio":
            query = DBM.parseLaboratorio(params)
        if table.lower() == "mensaje":
            query = DBM.parseMensaje(params)
        if table.lower() == "protocolos":
            query = DBM.parseProtocolos(params)
        if table.lower() == "zona_brote":
            query = DBM.parseZonaBrote(params)
        if table.lower() == "zoologicas":
            query = DBM.parseZoologicas(params)
        if table.lower() == "auditoria":
            query = DBM.parseAuditoria(params)

        #Si no hay parametros, retornamos None.
        if query is None:
            return None

        return "SELECT " + query + " FROM " + table + ";" 


    #Parsear los parametros para la consulta en tabla Personal
    @staticmethod
    def parserPersonal(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["id_empleado"] is True:
            query = query + "id_empleado,"
        if params["nombre_empleado"] is True:
            query = query + "nombre_empleado,"
        if params["apellido_empleado"] is True:
            query = query + "apellido_empleado,"
        if params["nivel_autorizacion"] is True:
            query = query + "nivel_autorizacion,"
        if params["superior_id"] is True:
            query = query + "superior_id,"
        if params["laboratorio_codigo"] is True:
            query = query + "laboratorio_codigo,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros para la consulta en la tabla Armamento.
    @staticmethod
    def parseArmemento(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["id_armamento"] is True:
            query = query + "id_armamento,"
        if params["nombre_armamento"] is True:
            query = query + "nombre_armamento,"
        if params["descripcion_armamento"] is True:
            query = query + "descripcion_armamento,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla BOW.
    @staticmethod
    def parseBow(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["codigo_lote"] is True:
            query = query + "codigo_lote,"
        if params["nombre_clave"] is True:
            query = query + "nombre_clave,"
        if params["fecha_mutacion"] is True:
            query = query + "fecha_mutacion,"
        if params["laboratorio_codigo"] is True:
            query = query + "laboratorio_codigo,"
        if params["cepa_id"] is True:
            query = query + "cepa_id,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Cepa_Viral.
    @staticmethod
    def parseCepaViral(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["id_cepa"] is True:
            query = query + "id_cepa,"
        if params["nombre_cepa"] is True:
            query = query + "nombre_cepa,"
        if params["descripcion_cepa"] is True:
            query = query + "descripcion_cepa"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Comunicaciones.
    @staticmethod
    def parseComunicaciones(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["fecha_envio"] is True:
            query = query + "fecha_envio,"
        if params["prioridad"] is True:
            query = query + "prioridad,"
        if params["mensaje_id"] is True:
            query = query + "mensaje_id,"
        if params["laboratorio_dest"] is True:
            query = query + "laboratorio_dest,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Despliegues.
    @staticmethod
    def parseDespliegues(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["clave_despliegue"] is True:
            query = query + "clave_despliegues,"
        if params["fecha_despliegue"] is True:
            query = query + "fecha_despliegue,"
        if params["num_especimenes"] is True:
            query = query + "num_especimenes,"
        if params["equipo_codigo"] is True:
            query = query + "equipo_codigo,"
        if params["geografico_id"] is True:
            query = query + "geografico_id,"
        if params["empleado_id"] is True:
            query = query + "empleado_id,"
        if params["lote_codigo"] is True:
            query = query + "lote_codigo"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Equipo_Contencion.
    @staticmethod
    def parseEquipoContencion(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["codigo_equipo"] is True:
            query = query + "codigo_equipo,"
        if params["nombre_equipo"] is True:
            query = query + "nombre_equipo,"
        if params["armamento_id"] is True:
            query = query + "armamento_id,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Especie_Animal.
    @staticmethod
    def parseEspecieAnimal(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["id_especie"] is True:
            query = query + "id_especie,"
        if params["nombre_especie"] is True:
            query = query + "nombre_especie,"
        if params["descripcion_especie"] is True:
            query = query + "descripcion_especie,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Estado_Cuarentena.
    @staticmethod
    def paseEstadoCuarentena(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["id_estado"] is True:
            query = query + "id_estado,"
        if params["nombre_estado"] is True:
            query = query + "nombre_estado,"
        if params["descripcion_estado"] is True:
            query = query + "descripcion_estado,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Humanoides.
    @staticmethod
    def parseHumanoides(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["valor_iq"] is True:
            query = query + "valor_iq,"
        if params["resistencia_daño"] is True:
            query = query + "resistencia_daño,"
        if params["lote_codigo"] is True:
            query = query + "lote_codigo,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta de la tabla Laboratorio.
    @staticmethod
    def parseLaboratorio(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["codigo_laboratorio"] is True:
            query = query + "codigo_laboratorio,"
        if params["nombre_clave"] is True:
            query = query + "nombre_clave,"
        if params["metros_profundidad"] is True:
            query = query + "metros_profundidad,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Mensaje.
    @staticmethod
    def parseMensaje(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["id_mensaje"] is True:
            query = query + "id_mensaje,"
        if params["laboratorio_org"] is True:
            query = query + "laboratorio_org,"
        if params["texto_mensaje"] is True:
            query = query + "texto_mensaje,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Protocolos.
    @staticmethod
    def parseProtocolos(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["num_protocolo"] is True:
            query = query + "num_protocolo,"
        if params["tiemp_cuenta_regresiva"] is True:
            query = query + "tiemp_cuenta_regresiva,"
        if params["cod_activacion_alfa"] is True:
            query = query + "cod_activacion_alfa,"
        if params["descripcion_protocolo"] is True:
            query = query + "descripcion_protocolo,"
        if params["laboratorio_codigo"] is True:
            query = query + "laboratorio_codigo,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Zona_Brote.
    @staticmethod
    def parseZonaBrote(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["id_geografico"] is True:
            query = query + "id_geografico,"
        if params["nombre_zona"] is True:
            query = query + "nombre_zona,"
        if params["estado_id"] is True:
            query = query + "estado_id,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.


    #Parsear los parametros de la consulta en la tabla Zoologicas.
    @staticmethod
    def parseZoologicas(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["tasa_agresividad"] is True:
            query = query + "tasa_agresividad,"
        if params["lote_codigo"] is True:
            query = query + "lote_codigo,"
        if params["especie_id"] is True:
            query = query + "especie_id,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.
    

    #Parsear los parametros de la consulta en la tabla Auditoria.
    @staticmethod
    def parseAuditoria(params:dict):
        if params is None:
            return None

        #Creamos el texto de la consulta
        query = ","

        #Concatenamos los parametros
        if params["fecha_registro"] is True:
            query = query + "fecha_registro,"
        if params["num_total_especimenes"] is True:
            query = query + "numero_total_especimenes,"
        if params["geografico_id"] is True:
            query = query + "geografico_id,"
    
        if len(query) <= 1: #Si solo esta "," no se parametrizo, return None.
            return None
    
        return query[1:-1] #Slice sin los indices 0 y n-1.

    