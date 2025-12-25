import json
import os


class ModellLeser:
    
    @staticmethod
    def lade_modelle(datei_name):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # Vollständiger Pfad zur JSON-Datei
        json_path = os.path.join(current_dir, datei_name)
        with open(json_path) as f:
            return json.load(f)

    @staticmethod
    def get_beschreibung(modelle, modellname):
        return modelle[modellname]['Beschreibung']

    @staticmethod
    def get_mikroorganismus(modelle, modellname):
        return modelle[modellname]['Mikroorganismus']

    @staticmethod
    def get_substrat_1(modelle, modellname):
        return modelle[modellname]['Substrat 1']

    @staticmethod
    def get_substrat_2(modelle, modellname):
        return modelle[modellname]['Substrat 2']

    @staticmethod
    def get_produkt_1(modelle, modellname):
        return modelle[modellname]['Produkt 1']

    @staticmethod
    def get_umax(modelle, modellname):
        return modelle[modellname]['umax']

    @staticmethod
    def get_ks_s1x(modelle, modellname):
        return modelle[modellname]['Ks_s1x']

    @staticmethod
    def get_ks_s2x(modelle, modellname):
        return modelle[modellname]['Ks_s2x']

    @staticmethod
    def get_yxs1(modelle, modellname):
        return modelle[modellname]['Yxs1']

    @staticmethod
    def get_yxs2(modelle, modellname):
        return modelle[modellname]['Yxs2']

    @staticmethod
    def get_ks_ox(modelle, modellname):
        return modelle[modellname]['ks_ox']

    @staticmethod
    def get_rq(modelle, modellname):
        return modelle[modellname]['RQ']

    @staticmethod
    def get_yxox(modelle, modellname):
        return modelle[modellname]['Yxox']

    @staticmethod
    def get_produktbildung(modelle, modellname):
        return modelle[modellname]['Produktbildung']

    @staticmethod
    def get_ap(modelle, modellname):
        return modelle[modellname]['ap']

    @staticmethod
    def get_bp(modelle, modellname):
        return modelle[modellname]['bp']

    @staticmethod
    def get_kp_max(modelle, modellname):
        return modelle[modellname]['kp_max']

    @staticmethod
    def get_km_s1p(modelle, modellname):
        return modelle[modellname]['km_s1p']

    @staticmethod
    def get_ypx_mu(modelle, modellname):
        return modelle[modellname]['Ypx_mu']

    @staticmethod
    def get_dichte_bruehe(modelle, modellname):
        return modelle[modellname]['Dichte Bruehe']

    @staticmethod
    def get_dyn_viscosity(modelle, modellname):
        return modelle[modellname]['dyn. Viscosity']

    @staticmethod
    def get_temp_in_c(modelle, modellname):
        return modelle[modellname]['Temp. In C']
