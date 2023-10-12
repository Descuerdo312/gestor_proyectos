from flask import Flask, render_template, request, redirect,url_for, session
from confi import conexion
from bd import Usuarios, Productos
from bson import ObjectId

bd = conexion()

app = Flask(__name__)
app.secret_key = 'ron'


def obtener_lideres():
    lideres = bd['Usuarios'].find({'cargo': 'lider'})
    return [usuario['nombre'] for usuario in lideres]

def obtener_miembros():
    miembros = bd['Usuarios'].find({'cargo': 'miembro'})
    return [usuario['nombre'] for usuario in miembros]

#--------------------------------------
@app.route("/ver_usuarios")
def ver_usuarios():
    # Filtrar los usuarios excluyendo los que tienen cargo 'jefe'
    usuarios = bd['Usuarios'].find({'cargo': {'$ne': 'jefe'}})
    
    return render_template("ver_usuarios.html", usuarios=usuarios)


@app.route("/editar_usuario/<id>")
def editar_usuario(id):
    usuario = bd['Usuarios'].find_one({'_id': ObjectId(id)})
    return render_template("editar_usuario.html", usuario=usuario)

@app.route("/eliminar_usuario/<id>")
def eliminar_usuario(id):
    bd['Usuarios'].delete_one({'_id': ObjectId(id)})
    return redirect(url_for("ver_usuarios"))

@app.route("/guardar_edicion_usuario", methods=['POST'])
def guardar_edicion_usuario():
    usuario_id = request.form['usuario_id']
    nuevo_nombre = request.form['nuevo_nombre']
    nuevo_correo = request.form['nuevo_correo']
    nuevo_password = request.form['nuevo_password']
    nuevo_cargo = request.form['nuevo_cargo']
    
    bd['Usuarios'].update_one({'_id': ObjectId(usuario_id)}, {'$set': {
        'nombre': nuevo_nombre,
        'correo': nuevo_correo,
        'password': nuevo_password,
        'cargo': nuevo_cargo
    }})
    
    return redirect(url_for("ver_usuarios"))

#--------------------------------------
@app.route("/ingresar")
def ingresarE():
    lideres = obtener_lideres()
    miembros = obtener_miembros()
    return render_template("ingresar.html", lideres=lideres, miembros=miembros)

@app.route("/guardar_personas", methods=['POST'])
def agregarUsuarios():
    nombre = request.form['nombre']
    correo = request.form['correo']
    password = request.form['password']
    cargo=request.form["cargo"]
    
    if nombre and correo and password and cargo: 
        usuario = Usuarios(nombre=nombre, correo=correo, password=password, cargo=cargo)
        bd['Usuarios'].insert_one(usuario.formato_doc())
        return redirect(url_for("iniciar_sesion"))
    else:
        return "error"

@app.route("/guardar_producto", methods=['POST'])
def agregarProducto():
    nombre_producto = request.form['nombre_producto']
    descripcion_proyecto = request.form['descripcion_proyecto']
    estado_proyecto = request.form['estado_proyecto']
    nivel_prioridad = request.form['nivel_prioridad']
    tareas = request.form['tareas'].split(',')
    Documentacion = request.form['Documentacion']
    lider_equipo = request.form['lider_equipo']
    miembros_equipo = request.form.getlist('miembros_equipo')
    fecha_inicio = request.form['fecha_inicio']
    fecha_final = request.form['fecha_final']


    if nombre_producto and descripcion_proyecto and estado_proyecto and nivel_prioridad and tareas and Documentacion and lider_equipo and miembros_equipo and fecha_inicio and fecha_final: 
        producto = Productos(
            nombre_producto=nombre_producto,
            descripcion_proyecto=descripcion_proyecto,
            estado_proyecto=estado_proyecto,
            nivel_prioridad=nivel_prioridad,
            tareas=tareas,
            Documentacion=Documentacion,
            lider_equipo=lider_equipo,
            miembros_equipo=miembros_equipo,
            fecha_inicio=fecha_inicio,
            fecha_final=fecha_final,

        )
        bd['Productos'].insert_one(producto.formato_doc())
        return redirect(url_for("visualizar"))
    else:
        return "error"

@app.route("/iniciar_sesion", methods=['POST'])
def iniciar_sesion():
    correo = request.form['correo']
    password = request.form['password']
    usuario_encontrado = bd['Usuarios'].find_one({'correo': correo, 'password': password})

    if usuario_encontrado:
        session['correo_actual'] = correo  # Guardamos el correo en la sesión
        cargo = usuario_encontrado.get('cargo')
        session['cargo'] = cargo
        print(f'El usuario tiene el cargo: {cargo}')  # Agregamos esta línea para imprimir el cargo
        if cargo == 'lider' or cargo == 'monitor de proyectos':
            return redirect(url_for("visualizar"))  # Redirigimos a la página de visualización
        elif cargo == 'Jefe':
            return redirect(url_for("panelJ"))  # Redirigimos a la página del líder
        else:
            return redirect(url_for("ver_mis_tareas"))  # Redirigimos a la página de tareas del usuario
    else:
        return "Error de autenticación. Inténtalo de nuevo."


@app.route("/visualizar")
def visualizar():
    productos = bd['Productos'].find()
    return render_template("visualizar.html", productos=productos)

@app.route("/editar_proyecto", methods=['GET'])
def editar_proyecto():
    producto_id = request.args.get('id')  
    producto = bd['Productos'].find_one({'_id': ObjectId(producto_id)})  

    lideres = obtener_lideres()  # Asegúrate de obtener los líderes aquí
    miembros = obtener_miembros()  # Asegúrate de obtener los miembros aquí

    return render_template("editarP.html", producto=producto, lideres=lideres, miembros=miembros)

#--------------------------------------------------------------
@app.route("/guardar_edicion", methods=['POST'])
def guardar_edicion():
    producto_id = request.form['producto_id']
    nombre_producto = request.form['nombre_producto']
    descripcion_proyecto = request.form['descripcion_proyecto']
    estado_proyecto = request.form['estado_proyecto']
    nivel_prioridad = request.form['nivel_prioridad']
    tareas = request.form['tareas'].split(',')
    Documentacion = request.form['Documentacion']
    lider_equipo = request.form['lider_equipo']
    miembros_equipo = request.form.getlist('miembros_equipo')
    fecha_inicio = request.form['fecha_inicio']
    fecha_final = request.form['fecha_final']
    
    bd['Productos'].update_one({'_id': ObjectId(producto_id)}, {'$set': {
        'nombre_producto': nombre_producto,
        'descripcion_proyecto': descripcion_proyecto,
        'estado_proyecto': estado_proyecto,
        'grado_de_prioridad': nivel_prioridad,
        'tareas': tareas,
        'documentación': Documentacion,
        'lider_del_equipo': lider_equipo,
        'miembros_del_equipo': miembros_equipo,
        'fecha_inicio': fecha_inicio,
        'fecha_final': fecha_final,
    }})

    return redirect(url_for("visualizar"))
#...................................................
@app.route("/eliminar_proyecto/<id>")
def eliminar_proyecto(id):
    bd['Productos'].delete_one({'_id': ObjectId(id)})
    return redirect(url_for("visualizar"))

#tareas----------------
@app.route("/ver_mis_tareas")
def ver_mis_tareas():
    # Obtener el correo del usuario actual desde la sesión
    correo_actual = session.get('correo_actual')
    
    # Buscar el usuario en la base de datos
    usuario = bd['Usuarios'].find_one({'correo': correo_actual})
    
    if usuario:
        tareas = usuario.get('tareas', [])
        return render_template("tareas.html", usuario=usuario, tareas=tareas)
    else:
        return "Usuario no encontrado"
@app.route("/enviar_tarea", methods=['POST'])
def enviar_tarea():
    tarea_nombre = request.form['nombre_tarea']
    correo_encargado = request.form['correo_encargado']
    respuesta = request.form['respuesta']

    # Obtener el producto y actualizar los reportes
    producto = bd['Productos'].find_one({'tareas': tarea_nombre})
    
    if producto:
        for idx, tarea in enumerate(producto['tareas']):
            if tarea == tarea_nombre:
                if 'reportes' not in producto:
                    producto['reportes'] = []

                producto['reportes'].append({
                    'tarea': tarea_nombre,
                    'encargado': correo_encargado,
                    'respuesta': respuesta
                })

                bd['Productos'].update_one({'_id': producto['_id']}, {'$set': {'reportes': producto['reportes']}})

                return redirect(url_for("ver_mis_tareas", correo=correo_encargado))
    return "Producto no encontrado"

@app.route("/asignar_tareas", methods=['POST'])
def asignar_tareas():
    tareas_asignadas = request.form.getlist('encargados')
    informes = request.form.getlist('informe')  # Obtener los informes

    # Obtén el producto y actualiza las tareas asignadas e informes
    producto_id = request.form['producto_id']
    bd['Productos'].update_one({'_id': ObjectId(producto_id)}, {'$set': {'tareas_asignadas': tareas_asignadas, 'informes': informes}})
    
    return redirect(url_for("visualizar"))

#fin tareas----------
@app.route("/detalles_proyecto/<id>")
def detalles_proyecto(id):
    producto = bd['Productos'].find_one({'_id': ObjectId(id)})

    return render_template("detalles_proyecto.html", producto=producto)

@app.route("/editar_eliminar_personal")
def editar_eliminar_personal():
    return render_template("edyelP.html")

@app.route("/panelJ")
def panelJ():
    return render_template("panelJ.html")

@app.route("/ingresar")
def ingresar():
    return render_template("ingresar.html")

@app.route("/crear_usuario")
def crear_usuario():
    return render_template("crearu.html")

@app.route("/iniciar_sesion")
def visitantes():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
