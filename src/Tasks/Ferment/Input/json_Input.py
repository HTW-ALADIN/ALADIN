import os
import json
from Input.inputBaseClass import InputBase

class JsonInput(InputBase):



    def __init__(self,datei_name):  #Konstruktor
        self.__jsonName = datei_name # private variable

    # Deklaration des Attributs außerhalb des Konstruktors
    __data = None

    def set_data(self,data):
        self.__data=data
    
    def get_data(self):
        return self.__data
    
    def get_jsonName(self):
        return self.__jsonName

    def set_jsonName(self, value):
        self.__jsonName = value





    def find_pfad(self):
        root_directory = os.path.abspath('src/Tasks/Ferment')  # Den absoluten Pfad des Projektnamens ermitteln

        for root, dirs, files in os.walk(root_directory):
            for file in files:
                if file.lower() == self.__jsonName.lower():  # Wenn die Datei gefunden wurde
                    return os.path.join(root, file)  # Dateipfad zurückgeben, sobald die Datei gefunden wurde
        return None  # Wenn die Datei nicht gefunden wurde, wird None zurückgegeben


    def ladeJson(self):
        # Vollständiger Pfad zur JSON-Datei
        json_path = self.find_pfad()
        if json_path is None : 
            print('Pfad zur Datei nicht gefunden.!!!')
            return None
        
        print('Datei gefunden:', json_path)  # Fügen Sie Debugging-Ausgabe hinzu
        try:
            # Öffne die JSON-Datei und lade sie
            with open(json_path, 'r') as file:
                data = json.load(file)
            self.set_data(data)
            
        except FileNotFoundError:
            print(f"Die Datei '{self.__jsonName}' konnte nicht geladen werden.")
            return None
    

    def get_Value(self):
        '''
        parameter = None
        parameter = list(self.__data.keys())[0]

        if parameter == None : 
            print('Error : Fehler beim Einlesen des Parameters.')
        
        if isinstance(self.__data[parameter][element], dict):
            element_dict = self.__data[parameter][element]
            value =  list(element_dict.items())[1]
            value = value[1]
            
        else :
            value = self.__data[parameter][element]
        

        
        if isinstance(value, int):
            return value
        elif isinstance(value,str):
            return value
        elif isinstance(value,float):
            return value
        else : 
            array = [float(val) for val in value]
            return array'''
        # JSON-String zu Python-Dictionary konvertieren
        data = self.__data
        
        # Array initialisieren
        result = []
        
        for key, value in data.items():
            if isinstance(value, dict):
                result.extend(list(value.values()))
            else:
                # Wenn der Wert kein Dictionary ist oder kein Array enthält
                result.append(value)
        
        for i, r in enumerate(result):
            if isinstance(r, int):
                result[i]=int(r)
            elif isinstance(r,list):
                result[i] = [float(val) for val in r]
        
        return result
