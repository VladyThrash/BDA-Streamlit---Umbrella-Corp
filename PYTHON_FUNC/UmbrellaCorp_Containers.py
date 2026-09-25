# Vladimir Yepez Contreras - S23002520 - IINF.

#Descripción:
#   Se definiran objetos containers o contenedores para almacenar registros especificos. Imagina el registro usuario que tiene los campos 
#   id, nombre, apellido, ...  Su funcionalidad es envolver todos estos campos sin tener que trabajar con estructuras de datos como
#   listas o diccionarios. Piensese como tipos STRUCTS.


#Contenerdor de un registro "Personal"
class Personal:
    def __init__(self, id_empleado, nombre_empleado, apellido_empleado, nivel_autorizacion, superior_id, laboratorio_codigo):
        self.id_empleado = id_empleado
        self.nombre_empleado = nombre_empleado
        self.apellido_empleado = apellido_empleado
        self.nivel_autorizacion = nivel_autorizacion
        self.superior_id = superior_id
        self.laboratorio_codigo = laboratorio_codigo


#Contenedor de un registro "Equipo Contencion", más el armamento utilizado.
class EquipoContencion:
    def __init__(self, codigo_equipo, nombre_equipo, nombre_armamento):
        self.codigo_equipo = codigo_equipo
        self.nombre_equipo = nombre_equipo
        self.nombre_armamento = nombre_armamento


#Contenedor de un registro "Zona Brote", más el estado de la cuarentena en el lugar.
class ZonaBrote:
    def __init__(self, id_geografico, nombre_zona, nombre_estado):
        self.id_geografico = id_geografico
        self.nombre_zona = nombre_zona
        self.nombre_estado = nombre_estado


#Contenedor de un registro "B.O.W", más la información del tipo especifico.
class BOW:
    def __init__(self, codigo_lote, nombre_clave, fecha_mutacion, laboratorio_codigo, nombre_cepa, tipo, tasa_agresividad=None, nombre_especie=None, valor_iq=None, resistencia_daño=None):
        self.codigo_lote = codigo_lote
        self.nombre_clave = nombre_clave
        self.fecha_mutacion = fecha_mutacion
        self.laboratorio_codigo = laboratorio_codigo
        self.nombre_cepa = nombre_cepa
        self.tipo = tipo
        #Para el tipo Zoologico
        self.tasa_agresividad = tasa_agresividad
        self.nombre_especie = nombre_especie
        #Para el tipo Humanoide
        self.valor_iq = valor_iq
        self.resistencia_daño = resistencia_daño