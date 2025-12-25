import json
import os

class ParameterLeser:
    
    @staticmethod
    def lade_parameter(datei_name):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # Vollständiger Pfad zur JSON-Datei
        json_path = os.path.join(current_dir, datei_name)
        with open(json_path) as f:
            return json.load(f)['Parameter']

    @staticmethod
    def get_modell(parameter):
        return parameter['Modell']

    @staticmethod
    def get_phasenanzahl(parameter):
        return parameter['PhasenAnzahl']

    @staticmethod
    def get_dauer(parameter):
        return parameter['Dauer']['DauerArray']

    @staticmethod
    def get_druck(parameter):
        return parameter['Druck']['DruckArray']

    @staticmethod
    def get_drehzahl(parameter):
        return parameter['Drehzahl']['DrehzahlArray']

    @staticmethod
    def get_zuluft(parameter):
        return parameter['Zuluft']['ZuluftArray']

    @staticmethod
    def get_bolus_c(parameter):
        return parameter['BolusC']['BolusCArray']

    @staticmethod
    def get_futter(parameter):
        return parameter['Feed']['FeedArray']

    @staticmethod
    def get_bolus_n(parameter):
        return parameter['BolusN']['BolusNArray']

    @staticmethod
    def get_temperatur(parameter):
        return parameter['Temperatur']['temperatur']

    @staticmethod
    def get_start_biomasse(parameter):
        return parameter['Startbiomasse']['startbiomasse']

    @staticmethod
    def get_do(parameter):
        return parameter['DO']['do']