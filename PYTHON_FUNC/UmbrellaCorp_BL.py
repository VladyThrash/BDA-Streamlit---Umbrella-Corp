# Vladimir Yepez Contreras - S23002520 - IINF.

#Estructura:
#   - UmbrellaCorp_FP.py (FRONT PANEL) es la interfaz gráfica con la que interactuaran nuestros científicos (Vista del usuario), 
#     implementara las funciones y clases encargadas de la conexión a la BD y la lógica del negocio.
#   - UmbrellaCorp_DBM.py (DATA BASE MANAGER) es la encargada del manejo de la conexión a la BD (consultas, insersiones, transacciones, 
#     cifrado, etc). Su función solo obedece al trabajo en "crudo" de los datos.
#   - UmbrellaCorp_BL.py (BUSINESS LOGIC) se encarga del procesamiento de los datos en función a la lógica de negocio de Umbrella.
#     Permitira procesar información tanto para presentación (FRONT PANEL) como para almacenamiento (DATA BASE MANAGER).


#Importamos las librerías y clases necesarias para este módulo.
import pandas as pd
import graphviz
from UmbrellaCorp_DBM import DBM
from UmbrellaCorp_Containers import Personal
from UmbrellaCorp_Containers import EquipoContencion
from UmbrellaCorp_Containers import ZonaBrote
from UmbrellaCorp_Containers import BOW


#Creamos la clase BL (BUSINESS LOGIC), que recibe un objeto DBM (DATA BASE MANAGER) para obtener y procesar los datos en función a la lógica
#de negocio de Umbrella.
class BL:

    #El constructor de la clase recibe un objeto o instancia con conexión a la BD (El pool y sus métodos).
    #BL es como un "Usuario", ya que utiliza unicamente el hilo dado para hacer las consultas requeridas en el procesamiento de datos.
    def __init__(self, db:DBM = None):
        self.db = db


    #Obtener el registro especifico de un empleado dado su ID y el código del laboratorio.
    #Lógica de LOGIN del FRONT PANEL.
    def obtenerRegistroEmpleado(self, id_empleado:str = None, codigo_laboratorio:str = None) -> Personal:
        #Creamos el QUERY.
        if codigo_laboratorio is None:
            query = "SELECT * FROM Personal WHERE id_empleado = " + id_empleado + " AND laboratorio_codigo is NULL;" 
        else:
            query = "SELECT * FROM Personal WHERE id_empleado = " + id_empleado + " AND laboratorio_codigo = '" + codigo_laboratorio + "';" 

        #Le decimos al DBM que ejecute la consulta.
        res = self.db.executeSelectFromPool(query)

        #Validamos el resultado.
        if res is None or res == []:
            return None

        res_t = res[0] #Tenemos un unico registro (una tupla).
        return Personal(id_empleado= res_t[0],
                        nombre_empleado= res_t[1],
                        apellido_empleado= res_t[2],
                        nivel_autorizacion= res_t[3],
                        superior_id= res_t[4],
                        laboratorio_codigo= res_t[5]
                        )
        

    #Obtener solo los códigos de los laboratorios registrados.
    #Lógica del LOGIN del FRONT PANEL.
    def obtenerCodigosLabs(self):
        res = self.db.getLaboratorio(nombre_clave=False, metros_profundidad=False)
        labs = [row[0] for row in res] #Convertimos la lista de tuplas a una lista plana.
        labs.append("SN/Lab")
        return labs


    #Obtener a los jefes científicos (nivel_acceso >= 7).
    #Funcionalidad generica del FRONT PANEL.
    def obtenerJefesCientificos(self):
        #Creamos el Query
        query = "SELECT nombre_empleado, apellido_empleado FROM Personal WHERE nivel_autorizacion >= 7 AND laboratorio_codigo is not NULL;"
        
        #DBM ejecuta la consulta.
        res = self.db.executeSelectFromPool(query)

        #Validamos el resultado.
        if res is None or res == []:
            return None

        #Formateamos el texto.
        bosses = list()
        for row in res:
            bosses.append(row[0] + " " + row[1]) #Convertimos la lista de tuplas a una lista de strings.

        return bosses


    #Obtener el registro de Jefe Científico dado el nombre y el apellido.
    def obtenerRegistroJefe(self, nombre_empleado:str, apellido_empleado:str):
        #Creamos el Query.
        query = "SELECT * FROM Personal WHERE nombre_empleado like '" + nombre_empleado + "' AND apellido_empleado like '" + apellido_empleado + "' AND nivel_autorizacion >= 7 AND laboratorio_codigo is not NULL limit 1;"

        #DBM ejecuta la consulta
        res = self.db.executeSelectFromPool(query)
        
        #Validamos el resultado.
        if res is None or res == []:
            return None

        res_t = res[0] #Tenemos un unico registro (una tupla).
        return Personal(id_empleado= res_t[0],
                        nombre_empleado= res_t[1],
                        apellido_empleado= res_t[2],
                        nivel_autorizacion= res_t[3],
                        superior_id= res_t[4],
                        laboratorio_codigo= res_t[5]
                        )


    #Ontener la cadena de mando dado el ID de un jefe científico.
    def obtenerCadenaMando(self, id_empleado:int):
        #Cargamos el CTE recursivo previo del DBM.
        query = self.db.parseCTEQuery(id_empleado)

        #El DBM ejecuta la consulta.
        res = self.db.executeSelectFromPool(query)

        #Validamos el resultado.
        if res is None or res == []:
            return None

        #Crear el objeto de grafo dirigido (Digraph).
        graph = graphviz.Digraph(
            #Estilo corporativo a los nodos (cajas redondeadas).
            node_attr={'shape': 'box', 'style': 'filled,rounded', 'fillcolor': "#f6f4f0", 'fontname': 'sans-serif'}
        )

        #Obtenemos el ID del nodo raiz.
        id_root = res[0][0]

        #Desempaquetar los registros.
        for id_empleado, nombre_empleado, apellido_empleado, nivel_autorizacion, superior_id, profundidad in res:
            # Graphviz requiere que los IDs de los nodos sean cadenas de texto (str).
            nodo_id = str(id_empleado)

            #Saber la categoría del empleado.
            if nivel_autorizacion <= 3:
                category = "Técnico"
            elif nivel_autorizacion < 7:
                category = "Científico"
            else:
                category = "Jefe Científico"

            # Información del nodo.
            etiqueta = f"{nombre_empleado} {apellido_empleado}\nNivel: {nivel_autorizacion}\n {category}"
            
            # Agregamos el empleado como un nodo en el mapa.
            graph.node(name=nodo_id, label=etiqueta)
            
            # Trazamos las aristas del grafo.
            if id_empleado != id_root:
                graph.edge(tail_name=str(superior_id), head_name=nodo_id)

        return graph
        

    #Obtener el nombre_clave y el codigo_lote de los B.O.W's.
    def obtenerEspecimenes(self):
        res = self.db.getBOW(fecha_mutacion=False, laboratorio_codigo=False, cepa_id=False)

        #Validamos el resultado.
        if res is None or res == []:
            return None
        
        #Formateamos el texto.
        especimenes = list()
        for row in res:
            especimenes.append(row[1] + " ID: " + row[0]) #Convertimos la lista de tuplas a una lista de strings.
        
        return especimenes


    #Obtener el nombre_zona y el id_geografico de las Zonas de Brote.
    def obtenerZonasBrote(self):
        res = self.db.getZonaBrote(estado_id=False)

        #Validamos el resultado.
        if res is None or res == []:
            return None
        
        #Formateamos el texto.
        zonas = list()
        for row in res:
            zonas.append(row[1] + " ID: " + str(row[0])) #Convertimos la lista de tuplas a una lista de strings.
        
        return zonas


    #Obtener el nombre_equipo y codigo_equipo de los Equipos de Contención.
    def obtenerEquiposContencion(self):
        res = self.db.getEquipoContencion(armamento_id=False)

        #Validamos el resultado.
        if res is None or res == []:
            return None
        
        #Formateamos el texto.
        equipos = list()
        for row in res:
            equipos.append(row[1] + " ID: " + row[0]) #Convertimos la lista de tuplas a una lista de strings.
        
        return equipos


    #Registrar un nuevo despliegue utilizando STORED PROCEDURE.
    def registrarNuevoDespliegue(self, num_especimenes:int, equipo_codigo:str, geografico_id:int, empleado_id:int, lote_codigo:str)->str:
        #Creamos el query.
        query = f"CALL nuevo_despliegue({num_especimenes}, '{equipo_codigo}', {geografico_id}, {empleado_id}, '{lote_codigo}');"

        #El DBM ejecuta la consulta.
        return self.db.executeModifyFromPool(query= query, autocommit= True)


    #Obtener un registro de la tabla Equipo_Contencion dado su ID.
    def obtenerRegistroEquipoContencion(self, codigo_equipo:str):
        #Creamos el query.
        query = f"SELECT codigo_equipo, nombre_equipo, armamento.nombre_armamento FROM equipo_contencion JOIN armamento on equipo_contencion.armamento_id = armamento.id_armamento WHERE codigo_equipo like '{codigo_equipo}';"
        
        #El DBM ejecuta la consulta.
        res = self.db.executeSelectFromPool(query)

        #Validamos el resultado.
        if res is None or res == []:
            return None

        return EquipoContencion(res[0][0], res[0][1], res[0][2])


    #Obtener un registro de la tabla Zona_Brote dado su ID.
    def obtenerRegistroZonaBrote(self, id_geografico:str):
        #Creamos el query.
        query = f"SELECT id_geografico, nombre_zona, estado_cuarentena.nombre_estado FROM zona_brote JOIN estado_cuarentena on zona_brote.estado_id = estado_cuarentena.id_estado WHERE id_geografico = {id_geografico};"

        #El DBM ejecuta la consulta.
        res = self.db.executeSelectFromPool(query)

        #Validamos el resultado
        if res is None or res == []:
            return None

        return ZonaBrote(res[0][0], res[0][1], res[0][2])


    #Obtener un registro de la tabla BOW dado su ID.
    def obtenerRegistroBOW(self, codigo_lote: str):
        #Creamos el query usando LEFT JOINs para obtener los datos sin importar el tipo, 
        #y un CASE para definir el campo 'tipo' dinámicamente.
        query = f"""
            SELECT 
                b.codigo_lote, 
                b.nombre_clave, 
                b.fecha_mutacion, 
                b.laboratorio_codigo, 
                c.nombre_cepa,
                CASE 
                    WHEN h.lote_codigo IS NOT NULL THEN 'Humanoide'
                    WHEN z.lote_codigo IS NOT NULL THEN 'Zoologico'
                    ELSE 'Desconocido'
                END AS tipo,
                z.tasa_agresividad, 
                e.nombre_especie, 
                h.valor_iq, 
                h.resistencia_daño
            FROM BOW b
            LEFT JOIN Cepa_Viral c ON b.cepa_id = c.id_cepa
            LEFT JOIN Humanoides h ON b.codigo_lote = h.lote_codigo
            LEFT JOIN Zoologicas z ON b.codigo_lote = z.lote_codigo
            LEFT JOIN Especie_Animal e ON z.especie_id = e.id_especie
            WHERE b.codigo_lote = '{codigo_lote}';
        """

        #El DBM ejecuta la consulta.
        res = self.db.executeSelectFromPool(query)

        #Validamos el resultado
        if res is None or res == []:
            return None

        #Instanciamos el objeto BOW. 
        return BOW(
            res[0][0],  # codigo_lote
            res[0][1],  # nombre_clave
            res[0][2],  # fecha_mutacion
            res[0][3],  # laboratorio_codigo
            res[0][4],  # nombre_cepa
            res[0][5],  # tipo
            res[0][6],  # tasa_agresividad
            res[0][7],  # nombre_especie
            res[0][8],  # valor_iq
            res[0][9]   # resistencia_daño
        )


    #Obtener metricas genericas de la tabla Despliegues.
    def obtenerMetricasGenericas(self):
        #Creamos la consulta (num_especimenes_totales, num_zonas_criticas >= 4, num_equipos_desplegados).
        query = """
                SELECT sum(num_especimenes) as sum_esp, count(DISTINCT geografico_id) as count_geo, count(equipo_codigo) as count_team from Despliegues 
                JOIN zona_brote on despliegues.geografico_id = zona_brote.id_geografico
                WHERE zona_brote.estado_id >= 4;
        """

        #El DBM ejecuta la consulta.
        res = self.db.executeSelectFromPool(query)

        #Validamos el resultado.
        if res is None or res == []:
            return None

        return res[0] #Retornamos la tupla (num_especimenes_totales, num_zonas_criticas >= 4, num_equipos_desplegados).


    #Obtener número de B.O.W's desplegados por especie.
    def obtenerMetricasBOW(self):
        #Creamos el query.
        query = """
            SELECT 
                b.nombre_clave AS nombre_bow,
                SUM(d.num_especimenes) AS total_desplegados
            FROM Despliegues d
            JOIN BOW b ON d.lote_codigo = b.codigo_lote
            GROUP BY b.nombre_clave
            ORDER BY total_desplegados DESC;
        """
        res = self.db.executeSelectFromPool(query)
        columnas = ['Especie', 'Total_Desplegados']
        
        if not res:
            return pd.DataFrame(columns=columnas)
            
        return pd.DataFrame(res, columns=columnas)


    #Obtener tipo de cuarentena por zona y equipo de contención encargado.
    def obtenerMetricasZonasDespliegue(self):
        #Creamos el query.
        #Usamos DISTINCT porque un mismo equipo podría tener múltiples despliegues en la misma zona, y solo queremos el mapeo único.
        query = """
            SELECT DISTINCT
                zb.nombre_zona,
                ec.nombre_estado AS tipo_cuarentena,
                eq.nombre_equipo AS equipo_encargado,
                zb.latitud AS lat,
                zb.longitud AS lon
            FROM Despliegues d
            JOIN Zona_Brote zb ON d.geografico_id = zb.id_geografico
            JOIN Estado_Cuarentena ec ON zb.estado_id = ec.id_estado
            JOIN Equipo_Contencion eq ON d.equipo_codigo = eq.codigo_equipo
            WHERE zb.latitud IS NOT NULL AND zb.longitud IS NOT NULL
            ORDER BY zb.nombre_zona;
        """
        res = self.db.executeSelectFromPool(query)
        columnas = ['Zona', 'Tipo_Cuarentena', 'Equipo_Contencion', 'lat', 'lon']
        
        if not res:
            return pd.DataFrame(columns=columnas)
            
        return pd.DataFrame(res, columns=columnas)


    #Obtenemos los tipos de espécimen por zona
    def obtenerMetricasDispersion(self):
        #Creamos el query.
        query = """
            SELECT 
                zb.nombre_zona,
                b.nombre_clave AS nombre_bow,
                SUM(d.num_especimenes) AS cantidad
            FROM Despliegues d
            JOIN Zona_Brote zb ON d.geografico_id = zb.id_geografico
            JOIN BOW b ON d.lote_codigo = b.codigo_lote
            GROUP BY zb.nombre_zona, b.nombre_clave
            ORDER BY zb.nombre_zona, cantidad DESC;
        """
        res = self.db.executeSelectFromPool(query)
        columnas = ['Zona', 'Tipo_Especimen', 'Cantidad']
        
        if not res:
            return pd.DataFrame(columns=columnas)
            
        return pd.DataFrame(res, columns=columnas)