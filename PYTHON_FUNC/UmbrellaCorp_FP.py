# Vladimir Yepez Contreras - S23002520 - IINF.

#Estructura:
#   - UmbrellaCorp_FP.py (FRONT PANEL) es la interfaz gráfica con la que interactuaran nuestros científicos (Vista del usuario), 
#     implementara las funciones y clases encargadas de la conexión a la BD y la lógica del negocio.
#   - UmbrellaCorp_DBM.py (DATA BASE MANAGER) es la encargada del manejo de la conexión a la BD (consultas, insersiones, transacciones, 
#     cifrado, etc). Su función solo obedece al trabajo en "crudo" de los datos.
#   - UmbrellaCorp_BL.py (BUSINESS LOGIC) se encarga del procesamiento de los datos en función a la lógica de negocio de Umbrella.
#     Permitira procesar información tanto para presentación (FRONT PANEL) como para almacenamiento (DATA BASE MANAGER).


#Importamos las librerías y clases necesarias para este módulo.
import streamlit as st
from UmbrellaCorp_DBM import DBM
from UmbrellaCorp_BL import BL
from UmbrellaCorp_Containers import Personal
from UmbrellaCorp_Containers import EquipoContencion
from UmbrellaCorp_Containers import ZonaBrote
from UmbrellaCorp_Containers import BOW


#Creamos el Pool de conexiones a la Base de Datos.
#Se utiliza el decorador porque Streamlit ejecuta secuencialmente (de arriba a abajo) este archivo, @st.cache_resource nos permite decirle
#al interprete "Oye, eso ya lo hiciste, utiliza lo que tenias en cache y no vuelvas a ejecutar esto".
@st.cache_resource
def inicializar_bd():
    #Credenciales de la BD.
    db_info = st.secrets["postgres"]

    return DBM(
        host= db_info["host"],
        database= db_info["database"],
        user= db_info["user"],
        password= db_info["password"],
        port= db_info["port"]
    )

database = inicializar_bd() #Obtenemos la instancia, se utiliza el pool ya existente.
logic = BL(database) #Creamos el objeto "logic" para poder procesar los datos de la DB.


#Configurar la página
st.set_page_config(
    page_title= "Umbrella Corp.",
    layout= "wide",   #Todo el ancho del navegador.
    initial_sidebar_state= "expanded"   #Estado de la barra lateral.
)


#LOGIN (Barra lateral).
# - Un input para el ID del empleado.
# - Un selector de códigos de laboratorio.
# - Un botón para ingresar con la combinación ID - Código Lab.
# - Regresa información del empleado y activa paneles de control según el nivel de seguridad.

#Inicializar variables de estado de sesión.
if "usuario" not in st.session_state:
    st.session_state.usuario = None #El objeto del ultimo usuario consultado.
    st.session_state.jefe = None #Objeto del ultimo jefe consultado.
    st.session_state.obj = None #Objeto para saber info antes de un despliegue.

# Barra lateral
with st.sidebar:
    st.header("LOGIN")

    #Input del ID.
    id_empleado = st.text_input(
        label="ID EMPLEADO: ",
        value="",
        placeholder="Ingresa tu ID aquí"
    )

    # selector de Código de Laboratorio.
    codigo_laboratorio = st.selectbox(
        label="Código del Laboratorio",
        options=logic.obtenerCodigosLabs() # Lista de los códigos de laboratorios.
    )

    #Botón para ejecutar la consulta.
    btn_ingresar = st.button("Ingresar")

#Lógica del botón.
if btn_ingresar:
    if id_empleado and codigo_laboratorio:
        if codigo_laboratorio == "SN/Lab": #No tiene código asignado, se manda como None.
            codigo_laboratorio = None
        obj_empleado = logic.obtenerRegistroEmpleado(id_empleado, codigo_laboratorio)
        if obj_empleado is not None:
            #Guardamos el éxito del login en la sesión.
            st.session_state.usuario = obj_empleado
        else:
            #Reseteamos si fallan los datos.
            st.session_state.usuario = None
            st.error("El registro seleccionado no existe")
    else:
        st.warning("Por favor completa ambos campos para ingresar.")


#Cuerpo de la página.
st.title("Umbrella Corp")
st.subheader("Panel de control")
st.divider() 


#Mostrar una ficha con la información del empleado.
def ficha_empleado():
    # st.container(border=True) crea un recuadro visual
    with st.container(border=True):
        st.subheader("Documento de Identidad ")
        
        # Dividimos el espacio: 1/3 para la imagen/icono y 2/3 para el texto
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Avatar generado por iniciales (API):
            st.image(f"https://api.dicebear.com/7.x/initials/svg?seed={st.session_state.usuario.nombre_empleado}", width=120)
            
        with col2:
            # Markdown para destacar los títulos en negrita
            # NOTA: Ajusta 'id_empleado' y 'codigo_laboratorio' a los nombres reales de los atributos de tu objeto
            st.markdown(f"**ID Empleado:** {st.session_state.usuario.id_empleado}")
            st.markdown(f"**Nombre:** {st.session_state.usuario.nombre_empleado}")
            st.markdown(f"**Apellido:** {st.session_state.usuario.apellido_empleado}")
            st.markdown(f"**Código Lab:** {st.session_state.usuario.laboratorio_codigo}")
            
        st.divider()
        col_metrica1, col_metrica2 = st.columns(2)
        col_metrica1.metric(label="Nivel de Autorización", value= f"Nivel {st.session_state.usuario.nivel_autorizacion}")

        #Saber la categoría del empleado
        if st.session_state.usuario.superior_id is None:
            category = "CEO"
        elif st.session_state.usuario.nivel_autorizacion <= 3:
            category = "Técnico"
        elif st.session_state.usuario.nivel_autorizacion < 7:
            category = "Científico"
        else:
            category = "Jefe Científico"

        col_metrica2.metric(label="Categoría", value= category)


#Mostrar un selector para buscar información sobre jefes de división científica.
def selector_jefe():
    with st.container(border=True):
        st.subheader("Jefes de división científica")

        #Dividimos el espacio en dos columnas (1 - selector y botón, 2 - información obtenida).
        col1, col2 = st.columns(2)

        with col1:
            #Selector y botón.
            jefe_cientifico = st.selectbox(
                label="Jefe Científico",
                options=logic.obtenerJefesCientificos() # Lista de los científicos jefes.
            )

            #Botón para ejecutar la consulta.
            btn_buscar = st.button("Buscar")

        #Si el botón fue pulsado, ejecutamos la consulta.
        if btn_buscar:
            params = jefe_cientifico.split()
            st.session_state.jefe = logic.obtenerRegistroJefe(params[0], params[1])

        with col2:
            #Información del jefe.
            if st.session_state.jefe is not None:
                st.markdown(f"**Nombre:** {st.session_state.jefe.nombre_empleado}")
                st.markdown(f"**Apellido:** {st.session_state.jefe.apellido_empleado}")
                st.markdown(f"**Código Lab:** {st.session_state.jefe.laboratorio_codigo}")

            else:
                st.info("Selecciona un jefe...")

        #Proyectamos el grafo de la cadena de mando resultante del jefe seleccionado.
        if st.session_state.jefe is not None:
            graph = logic.obtenerCadenaMando(st.session_state.jefe.id_empleado) #Hace la consulta y obtiene el objeto grafo.
            if graph is not None:
                st.divider()
                col_izq, col_centro, col_der = st.columns([1, 3, 1])
                with col_centro:
                    st.markdown("**Cadena de Mando**")
                    st.graphviz_chart(graph, use_container_width=True) #Renderizar el grafo.



#Un selector dinámico (con información ya existente - selectboxes) para registrar nuevos despliegues.
#A demas de un buscador interactivo para buscar más información sobre las zonas de brote, las B.O.W's y los equipos de contención.
def registro_despliegue():
    #Dividimos el espacio en dos columnas.
    col1, col2 = st.columns([2,1])

    #El forms de registro.
    with col1:
        with st.container(border=True):
            st.subheader("Formulario de Despliegues")

            #Declarar un st.form (persistencia).
            with st.form(key="registro_despliegue"):
                #Selector de especimen.
                especimen = st.selectbox(
                    label="B.O.W. - Espécimen",
                    options=logic.obtenerEspecimenes() #Lista de los espécimenes.
                )

                #Selector de región.
                zona_brote = st.selectbox(
                    label="Zona de Brote",
                    options=logic.obtenerZonasBrote() #Lista de las regiones de brote.
                )

                #Selector de equipo de contención.
                equipo_contencion = st.selectbox(
                    label="Equipo de Contención",
                    options=logic.obtenerEquiposContencion() #Lista de los equipos de contención.
                )

                #Slider de número de especimenes.
                num_especimenes = st.slider(
                    label= "Cantidad de espécimenes a desplegar",
                    min_value= 1,
                    max_value= 100,
                    value= 1,
                    step= 1,
                    help= "Indicar número de espécimenes para un nuevo despliegue"
                )
                
                #Botón de registro.
                boton_registrar = st.form_submit_button(label="Registrar despliegue")

            #Jalar todos los datos del forms.
            if boton_registrar:
                #Separamos los ID's de los nombres.
                p_especimen = especimen.split("ID: ")
                p_zona_brote = zona_brote.split("ID: ")
                p_equipo_contencion = equipo_contencion.split("ID: ")

                #Enviamos el nuevo registro.
                sys_msg = logic.registrarNuevoDespliegue(
                    num_especimenes= num_especimenes,
                    equipo_codigo= p_equipo_contencion[1],
                    geografico_id= int(p_zona_brote[1]),
                    empleado_id= st.session_state.usuario.id_empleado,
                    lote_codigo= p_especimen[1]
                )
                if sys_msg == "QUERY SUCCESS":
                    st.success(sys_msg)
                else:
                    st.error(sys_msg)

    #El forms de consulta
    with col2:
        with st.container(border=True):
            st.subheader("Consultar elementos a desplegar")

            #Forms de persistencia
            with st.form(key="consulta_despliegue"):
                #Selector de la tabla de origen.
                tabla = st.selectbox(
                    label="Registro de origen",
                    options=["EQUIPO_CONTENCION", "ZONA_BROTE", "BOW"]
                )

                #Input del ID del elemento.
                id_elemento = st.text_input(
                    label="ID Elemento: ",
                    value="",
                    placeholder="Ingresa el ID aquí"
                )

                #Botón de busqueda.
                boton_buscar = st.form_submit_button(label="Buscar elemento")

            #Jalar todos los datos del forms.
            if boton_buscar:
                #'res' es un objeto.
                if tabla == "EQUIPO_CONTENCION":
                    st.session_state.obj = logic.obtenerRegistroEquipoContencion(id_elemento) #Instancia EquipoContencion.
                if tabla == "ZONA_BROTE":
                    st.session_state.obj = logic.obtenerRegistroZonaBrote(id_elemento) #Instancia ZonaBrote.
                if tabla == "BOW":
                    st.session_state.obj = logic.obtenerRegistroBOW(id_elemento) #Instamcia BOW.

                #Validar:
                if st.session_state.obj is None or st.session_state.obj == []:
                    st.error(f"El elemento: {id_elemento} de la tabla: {tabla} no existe")

            #Validar antes de imprimir
            if st.session_state.obj is not None:
                #Imprimir los objetos.
                if isinstance(st.session_state.obj, EquipoContencion):
                    st.markdown(f"**Equipo:** {st.session_state.obj.nombre_equipo}")
                    st.markdown(f"**Aramamento:** {st.session_state.obj.nombre_armamento}")

                elif isinstance(st.session_state.obj, ZonaBrote):
                    st.markdown(f"**Zona:** {st.session_state.obj.nombre_zona}")
                    st.markdown(f"**ALERTA -** {st.session_state.obj.nombre_estado}")
                    
                elif isinstance(st.session_state.obj, BOW):
                    st.markdown(f"**Nombre Clave:** {st.session_state.obj.nombre_clave}")
                    st.markdown(f"**Fecha Mutación:** {st.session_state.obj.fecha_mutacion}")
                    st.markdown(f"**Cepa:** {st.session_state.obj.nombre_cepa}")
                    st.markdown(f"**Tipo:** {st.session_state.obj.tipo}")

                    #Cambian los parametros segun el tipo.
                    if st.session_state.obj.tipo == "Humanoide":
                        st.markdown(f"**IQ:** {st.session_state.obj.valor_iq}")
                        st.markdown(f"**Resistencia:** {st.session_state.obj.resistencia_daño}")
                    if st.session_state.obj.tipo == "Zoologico":
                        st.markdown(f"**Agresividad:** {st.session_state.obj.tasa_agresividad}")
                        st.markdown(f"**Especie Origen:** {st.session_state.obj.nombre_especie}")

                else:
                    st.error(f"No se reconoce el objeto: {type(st.session_state.obj)}")
            

#Mostrar metricas: BOW's activas, Zonas de cuarentena Críticas, Número de especimenes desplegados.
def mostrar_metricas():
    #Metricas especificas para jefes.
    if st.session_state.usuario.nivel_autorizacion >= 7:
        pass

    #Metricas genericas para usuarios normales.
    else:
        metrics = logic.obtenerMetricasGenericas()
        with st.container(border=True):
            st.subheader("Resumen de Despliegues") #(num_especimenes_totales, num_zonas_criticas >= 4, num_equipos_desplegados)

            #Creamos 3 columnas para alinear las metricas.
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    label= "Cantidad de especímenes en campo", 
                    value= metrics[0],
                    delta= "aumento",
                    delta_color="inverse"
                )

            with col2:
                st.metric(
                    label= "Número de regiones críticas (cuarentena nivel 4 o 5)", 
                    value= metrics[1], 
                    delta= "aumento",
                    delta_color="inverse"
                )

            with col3:
                st.metric(
                    label="Cantidad equipos desplegados", 
                    value= metrics[2], 
                    delta= "aumento", 
                    delta_color="inverse"
                )


#Mostrar menú dado el objeto obtenido de la consulta.
if st.session_state.usuario is not None:
    st.success(f"¡Hola {st.session_state.usuario.nombre_empleado}!")
    ficha_empleado() #Info del usuario.
    
    #Cientificos de alto nivel (Todas las funcionalidades).
    if st.session_state.usuario.nivel_autorizacion >= 7:
        # - st.form para generar un nuevo despliegue con SP.
        registro_despliegue()

        # - Gráficos interactivos de agregación temporal (especímenes liberados por mes semana y por tipo de mutágeno).
        # - Mapa o diagrama de zonas geográficas afectadas.
        # - Acceso total a las tablas.
    
    #Metricas de cada BOW.
    mostrar_metricas()

    #Aquí las funcionalidades para todos los tipos de usuarios (selector de jefe y grafo de jerarquías).
    selector_jefe()

    #Botón para cerrar sesión.
    if st.button("Cerrar sesión"):
        #Reiniciamos todos los objetos de la sesión.
        st.session_state.usuario = None
        st.session_state.jefe = None
        st.session_state.obj = None
        st.rerun() #Fuerza la recarga para limpiar la pantalla.
else:
    st.info("Ingresa a LOGIN para registrarte")

