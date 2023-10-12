# Usuarios
class Usuarios:
    def __init__(self, nombre, correo, password,cargo,tareas=None):
        self.nombre = nombre
        self.correo = correo
        self.password= password
        self.cargo=cargo
        self.tareas=tareas or []
    def BD(self):
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "password": self.password,
            "cargo": self.cargo,
            "tareas": self.tareas
            
            }
        
    def formato_doc(self):
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "password": self.password,
            "cargo":self.cargo,
            "tareas": self.tareas if hasattr(self, 'tareas') else []
        }

# Productos
class Productos: 
    def __init__(self, nombre_producto, descripcion_proyecto, estado_proyecto,
                 nivel_prioridad, tareas, Documentacion, lider_equipo, 
                 miembros_equipo, fecha_inicio, fecha_final, reportes=None):
        #----------------selfs--------------------------------
        self.nombre_producto = nombre_producto
        self.descripcion_proyecto = descripcion_proyecto
        self.estado_proyecto = estado_proyecto  
        self.nivel_prioridad = nivel_prioridad
        self.tareas = tareas
        self.Documentacion = Documentacion
        self.lider_equipo = lider_equipo
        self.miembros_equipo = miembros_equipo
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.reportes = reportes if reportes is not None else []
        #---------------------------------------------#
    def BD(self):
        return {
            "nombre_producto": self.nombre_producto,
            "descripcion": self.descripcion_proyecto,
            "estado_proyecto": self.estado_proyecto,
            "grado_de_prioridad": self.nivel_prioridad,
            "tareas": self.tareas,
            "documentación": self.Documentacion,
            "lider_del_equipo": self.lider_equipo,
            "miembros_del_equipo": self.miembros_equipo,
            "fecha_inicio": self.fecha_inicio,
            "fecha_final": self.fecha_final,
            "reportes": self.reportes
        }
        #----------------------------------------------#
    def formato_doc(self):
        return {
            "nombre_producto": self.nombre_producto,
            "descripcion": self.descripcion_proyecto,
            "estado_proyecto": self.estado_proyecto,
            "grado_de_prioridad": self.nivel_prioridad,
            "tareas": self.tareas if hasattr(self, 'tareas') else [],
            "documentación": self.Documentacion,
            "lider_del_equipo": self.lider_equipo,
            "miembros_del_equipo": self.miembros_equipo,
            "fecha_inicio": self.fecha_inicio,
            "fecha_final": self.fecha_final,
            "reportes": self.reportes
        }
