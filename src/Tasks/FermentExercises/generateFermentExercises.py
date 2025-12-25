import json
import numpy as np

from excel_export import export_to_excel
from json_to_excel import json_to_excel
from nebenrechnungen import Berechnung_der_Sauerstoffloeslichkeit
from nebenrechnungen import Berechnung_des_kla_Wertes
from nebenrechnungen import parameter


from berechnungen import berechnung_der_Tabelle1
from berechnungen import berechnung_der_Tabelle2
from berechnungen import berechnung_der_Tabelle3
from berechnungen import berechnung

from interne_daten.data_importieren import data_importieren_von_json

from Input.json_Input import JsonInput

# Example data for the variables
#c_ox_sat = 0.21  # Example value for oxygen saturation concentration
#t_combined = np.linspace(0, 10, 100)  # Example time data
#y_combined = np.random.rand(5, 100)  # Example concentration data with 5 different concentrations over time
#cum_feeding = np.cumsum(np.random.rand(100))  # Example cumulative feeding data

#c_ox_sat = None  # Oxygen saturation concentration
#t_combined = None  # Time data
#y_combined = None  # Concentration data
#cum_feeding = None  # Cumulative feeding data


 #Modelle aus modelle.jsom laden
# Modelle aus modelle.json laden

def generateFermentExercises():
    modelleOb = JsonInput('modelle.json')
    modelleOb.ladeJson()
    modelle  = modelleOb.get_data()

        # Zum Test im Meeting
    m = modelleOb.get_Value()

        # Input aus input.json laden
    eingabeOb = JsonInput('FrontendEingaben.json')
    eingabeOb.ladeJson()
    eingabe = eingabeOb.get_Value()

    # Berechnungen durchführen
    Sauerstoffoeslichkeit_array = Berechnung_der_Sauerstoffloeslichkeit(eingabe[1], eingabe[9], eingabe[3])
    kla_werte = Berechnung_des_kla_Wertes(Sauerstoffoeslichkeit_array, modelle, eingabe[4], eingabe[0], eingabe[5], eingabe[1])
    parameter_werte = parameter(Sauerstoffoeslichkeit_array, kla_werte, modelle, eingabe[1], eingabe[0])
    const_array = berechnung_der_Tabelle1(parameter_werte, eingabe[0], modelle, eingabe[5], eingabe[7], eingabe[1])
    t_ranges_array = berechnung_der_Tabelle2(eingabe[2], eingabe[1])
    param_array = berechnung_der_Tabelle3(const_array, eingabe[10], eingabe[6], eingabe[8], eingabe[11], eingabe[1]) #!eingabe[6] => BolusC ; param_array[i][1]=float(bolus_c[i]) param_array[i][2]=float(bolus_n[i])

    # Berechnung ausführen
    ergebnis = berechnung(t_ranges_array, param_array, const_array, eingabe[1],eingabe[12], eingabe[13], eingabe[14], eingabeOb.get_data())
    c_ox_sat, y_combined, t_combined, cum_feeding = ergebnis
    

    #Export Resultat in Excel-Datei
    #export_to_excel("model_result.xlsx", t_combined, y_combined, cum_feeding)
    #plot_visualisieren(c_ox_sat, y_combined, t_combined, cum_feeding)
    
    
if __name__ == "__main__":
    generateFermentExercises()