

from view import plot_visualisieren
from excel_export import export_to_excel

from nebenrechnungen import Berechnung_der_Sauerstoffloeslichkeit
from nebenrechnungen import Berechnung_des_kla_Wertes
from nebenrechnungen import parameter

from berechnungen import berechnung_der_Tabelle1
from berechnungen import berechnung_der_Tabelle2
from berechnungen import berechnung_der_Tabelle3
from berechnungen import berechnung

from interne_daten.data_importieren import data_importieren_von_json

from Input.json_Input import JsonInput




if __name__ == "__main__":

    #Modelle aus modelle.jsom laden
    modelleOb = JsonInput('modelle.json')
    modelleOb.ladeJson()
    modelle  = modelleOb.get_data()
    
    #Zum Test im Meeting
    m = modelleOb.get_Value()
    print(m)
    #modelle = data_importieren_von_json('Modelle.json')
    
    #Input aus input.json laden
    eingabeOb   =  JsonInput('input.json')
    eingabeOb.ladeJson()
    eingabe = eingabeOb.get_Value()
    print(eingabe)


    Sauerstoffoeslichkeit_array=Berechnung_der_Sauerstoffloeslichkeit(eingabe[1],eingabe[9],eingabe[3])
    
    
    kla_werte=Berechnung_des_kla_Wertes(Sauerstoffoeslichkeit_array,modelle,eingabe[4],eingabe[0],eingabe[5],eingabe[1])
    
    
    parameter_werte=parameter(Sauerstoffoeslichkeit_array,kla_werte,modelle,eingabe[1],eingabe[0])
    
    
    const_array=berechnung_der_Tabelle1(parameter_werte,eingabe[0],modelle,eingabe[5],eingabe[7],eingabe[1])
    
    
    t_ranges_array= berechnung_der_Tabelle2(eingabe[2],eingabe[1])
    
    
    param_array=berechnung_der_Tabelle3(const_array,eingabe[10],eingabe[6],eingabe[8],eingabe[11],eingabe[1])
    
    
    #Berechnung_ausführen
    ergebnis = berechnung(t_ranges_array, param_array, const_array,eingabe[1])
    c_ox_sat, y_combined, t_combined, cum_feeding = ergebnis
    

    #Export Resultat in Excel-Datei
    export_to_excel("model_result.xlsx", t_combined, y_combined, cum_feeding)


    #Darstellung ausgeben
    plot_visualisieren(c_ox_sat, y_combined, t_combined, cum_feeding)
    