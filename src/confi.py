from pymongo import MongoClient
import certifi


MONGO="mongodb+srv://Ronal:RonRojas31@cluster0.lehfgge.mongodb.net/"

certificado=certifi.where()

def conexion():
    try:              
        Client=MongoClient(MONGO, tlsCAFile=certificado)
        bd= Client["Usuarios"]
        bd=Client["Productos"]
    except ConnectionError:
        print("No se ha podido conectar a la base de datos")
    return bd