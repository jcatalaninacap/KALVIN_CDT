"""
Capa de controladores (Presentation Layer, PL):
Encargada de interactuar con el usuario.
"""
import os
from django.shortcuts import render
from .especialistasDal import MongoDBHandler
from .especialistaService import EspecialistaService
from .utils import leer_conexion

# Leer la configuración desde conexion.txt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, 'conexion.txt')

# leer archivo
"""
with open(config_path, 'r') as file:
    print(file.read())
"""
try:
    config = leer_conexion(config_path)
except FileNotFoundError:
    print("El archivo conexion.txt no se encuentra en la ruta especificada.")
    raise

# Configuración de MongoDB
DB_URI = config.get('DB_URI')
DB_NAME = config.get('DB_NAME')
COLLECTION_NAME = config.get('COLLECTION_NAME')

db_handler = MongoDBHandler(DB_URI, DB_NAME, COLLECTION_NAME)
especialista_service = EspecialistaService(db_handler)

def especialistas_view(request):
    especialistas = especialista_service.obtener_especialistas()
    especialista_seleccionado = request.GET.get("especialista_id", "todas")

    if especialista_seleccionado.isdigit():
        especialista_index = int(especialista_seleccionado) - 2
        if 0 <= especialista_index < len(especialistas):
            especialista_nombre = especialistas[especialista_index]["nombre"]
            data = especialista_service.obtener_datos(especialista_nombre)
            return render(request, "detalle_especialista.html", {
                "data": data,
                "especialista": especialista_nombre,
            })

    data = especialista_service.obtener_datos()
    return render(request, "especialistas.html", {
        "data": data,
        "especialistas": especialistas,
        "especialista_seleccionado": especialista_seleccionado,
    })

def leer_conexion(archivo):
    config = {}
    with open(archivo, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            config[key] = value
    return config
