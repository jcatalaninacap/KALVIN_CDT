from pymongo import MongoClient

"""
Capa de acceso a datos (Data Access Layer, DAL):
Encargada de interactuar con la base de datos.
"""

class MongoDBHandler:
    
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_distinct_especialistas(self):
        return self.collection.distinct("Especialista", {"Especialista": {"$exists": True}})

    def aggregate_pipeline(self, pipeline):
        return list(self.collection.aggregate(pipeline))
    
    def leer_configuracion_conexion(archivo):
        configuracion = {}
        try:
            with open(archivo, "r") as f:
                for linea in f:
                    clave, valor = linea.strip().split("=")
                    configuracion[clave] = valor
        except FileNotFoundError:
            raise Exception(f"El archivo {archivo} no fue encontrado.")
        except ValueError:
            raise Exception(f"Error al procesar el archivo {archivo}. Verifica el formato.")
        return configuracion

