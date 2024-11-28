
# utils.py
def leer_conexion(archivo):
    config = {}
    with open(archivo, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or '=' not in line:
                continue  # Ignorar líneas vacías o incorrectas
            key, value = line.split('=', 1)
            config[key] = value
    return config
