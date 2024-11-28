"""

Capa de lógica de negocio (Business Logic Layer, BLL):
Define las reglas de negocio y procesa los datos.

"""


class EspecialistaService:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def obtener_especialistas(self):
        especialistas_raw = self.db_handler.get_distinct_especialistas()
        return [{"id": str(idx), "nombre": e} for idx, e in enumerate(especialistas_raw, start=1) if e.strip()]

    def construir_pipeline(self, especialista=None):
        match_criteria = {
            "$and": [
                {"resolutionDate": {"$ne": "", "$exists": True}},
                {"Fecha de creacion": {"$ne": "", "$exists": True}},
            ]
        }
        if especialista:
            match_criteria["$and"].append({"Especialista": especialista})

        pipeline = [
            {"$match": match_criteria},
            {
                "$project": {
                    "Numero_de_ticket": "$Numero de ticket",
                    "Especialista": 1,
                    "Estado": 1,
                    "Tipo": 1,
                    "resolutionDate": 1,
                    "Fecha_de_creacion": "$Fecha de creacion",
                    "Fecha_de_modificacion": "$Fecha de modificacion",
                    "Tiempo_resolucion": {
                        "$round": [
                            {
                                "$divide": [
                                    {
                                        "$subtract": [
                                            {"$toDate": "$resolutionDate"},
                                            {"$toDate": "$Fecha de creacion"},
                                        ]
                                    },
                                    1000 * 60,
                                ]
                            },
                            2,
                        ]
                    },
                }
            },
        ]
        return pipeline

    def obtener_datos(self, especialista=None):
        pipeline = self.construir_pipeline(especialista)
        return self.db_handler.aggregate_pipeline(pipeline)
