"""
Capa de controladores (Presentation Layer, PL):
Encargada de interactuar con el usuario.
"""
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .especialistasDal import MongoDBHandler
from .especialistaService import EspecialistaService
from .utils import leer_conexion
from .desempenoService import DesempenoService
import matplotlib

matplotlib.use('Agg')

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

            # Generar gráfico
            desempeno_service = DesempenoService(db_handler)
            # Calcula las métricas para el especialista seleccionado
            #data_grafico = desempeno_service.calcular_metricas(especialista_nombre)
            grafico = generar_grafico(data,especialista_nombre)

            # Incluir gráfico en el contexto
            return render(request, "detalle_especialista.html", {
                "data": data,
                "especialista": especialista_nombre,
                "grafico": grafico,  # Agregado
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



def generar_grafico(data,especialista_nombre):
    especialistas = especialista_nombre
    cau = [item.get("Numero_de_ticket") for item in data]
    tiempos = [item.get("Tiempo_resolucion", 0) or 0 for item in data]

    plt.figure(figsize=(10, 5))
    plt.bar(cau, tiempos, color='blue', width=1.8)
    plt.xlim(-0.5, len(cau) - 0.5)  # Amplía los límites del eje X
    plt.title('Tiempo de Resolución por Especialista')
    plt.xlabel('Ticket')
    plt.ylabel('Horas')
    
    # Ocultar las etiquetas del eje X
    plt.xticks([])  
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return grafico_base64




