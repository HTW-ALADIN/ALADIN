

#Dictionary Henry_Konstanten erstellen
Henry_Kosntanten = {
    "Solut_KH1" :{  #L*atm*mol-1
        "O2"    : 769.2,
        "CO2"   : 29.41,
        "H2"    : 1282.1
    },

    "Solut_KH2" :{  #(L*bar)/mol
        "O2"    :   779.3919,
        "CO2"   :   29.7996825,
        "H2"    :   1299.087825    
    },

    "Solut_T"   :{  #in k
        "O2"    :   298.15,
        "CO2"   :   198.15,
        "H2"    :   298.15
    }
}

##Dictionary Temperaturkoeffizient erstellen

Temperaturkoeffizient   =   {   #Solut:C in K
    "O2"    :   1700,
    "H2"    :   500,
    "CO2"   :   2400,
    "N2"    :   1300,
    "He"    :   230,
    "Ne"    :   490,
    "Ar"    :   1300,
    "CO"    :   1300
}

#Dictionary für die Konstanten für P begast

Konstanten_fuer_P_begast = {
    "1" :   750,     #"Anzahl der Impeller/Rührorgane"   :   Konstante A in Pg Formel   
    "2" :   490,
    "3" :   375
}