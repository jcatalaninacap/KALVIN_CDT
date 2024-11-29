from datetime import datetime

class DesempenoService:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def calcular_metricas(self, especialista_nombre=None):
        match_criteria = {"estado": "cerrado"}
        if especialista_nombre:
            match_criteria["Especialista"] = especialista_nombre

        pipeline = [
            {"$match": match_criteria},
            {
                "$project": {
                    "ticket_id": 1,
                    "especialista": "$Especialista",
                    "tiempo_resolucion": {
                        "$divide": [
                            {"$subtract": ["$fecha_cierre", "$fecha_creacion"]},
                            1000 * 60 * 60,
                        ]
                    },
                    "cumplimiento_sla": {"$lte": ["$tiempo_resolucion", "$sla"]}
                }
            },
        ]
        
        return list(self.db_handler.aggregate_pipeline(pipeline))

