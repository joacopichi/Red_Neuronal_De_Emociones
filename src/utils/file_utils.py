import json
import os

def guardar_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def cargar_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []
