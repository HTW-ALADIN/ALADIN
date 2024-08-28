
import json
import os

def data_importieren_von_json(datei_name):
    # Verzeichnis des aktuellen Skripts
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # Vollständiger Pfad zur JSON-Datei
    json_path = os.path.join(current_dir, datei_name)

    try:
        # Öffne die JSON-Datei und lade sie
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Die Datei '{datei_name}' wurde nicht gefunden.")
        return None
