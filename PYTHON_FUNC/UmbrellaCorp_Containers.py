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