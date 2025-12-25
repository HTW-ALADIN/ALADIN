import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
import json

from Input.json_Input import JsonInput


# === Reaktionssystem ===
def reaktionssystem(t, y):
    cH2O2, cH2O, cO2 = y
    nH2O2 = cH2O2 * v
    UH2O2 = (nH2O2_0 - nH2O2) / nH2O2_0
    T = T_Start + dTad * UH2O2
    k = 0.000047 * T**2 - 0.0033484 * T + 0.0629815
    r_H2O2 = -k * cH2O2
    return [r_H2O2, -r_H2O2, -0.5 * r_H2O2]

# === Abbruchbedingung ===
def abbruch_bedingung(t, y):
    cH2O2 = y[0]
    nH2O2 = cH2O2 * v
    UH2O2 = (nH2O2_0 - nH2O2) / nH2O2_0
    return 0.95 - UH2O2




# read user inputs
userInputObject =   JsonInput('FrontendEingaben.json')
userInputObject.ladeJson()
userInputs      =   userInputObject.get_data()

phaseNumber     =   userInputs['phaseNumber']
process         =   userInputs['process']
matrixDataObj   =   userInputs['matrixData']



VH2O2_AS        =   matrixDataObj['VH2O2_AS'][0]       # Liter – Volumen H2O2 Zugabe in Reaktor
cH2O2_AS        =   matrixDataObj['CH2O2_AS'][0]      # mol/L – Konzentration H2O2 Zugabe
V_Start         =   matrixDataObj['V_Start'][0]        # Liter – Wasser-Startvolumen
T_Start         =   matrixDataObj['T_Start'][0]       # °C – Starttemperatur


'''
# === Nutzereingaben ===
VH2O2_AS = 5.0       # Liter – Volumen H2O2 Zugabe in Reaktor
cH2O2_AS = 12.0      # mol/L – Konzentration H2O2 Zugabe
V_Start = 100        # Liter – Wasser-Startvolumen
T_Start = 25.0       # °C – Starttemperatur
'''

# === Berechnungen ===
nH2O2_AS = cH2O2_AS * VH2O2_AS
cH2O2_Start = nH2O2_AS / V_Start
dTad = (cH2O2_Start * 98.2) / (4.19 * 2 * 1)

# === Startbedingungen ===
cH2O2_0 = cH2O2_Start
cH2O_0 = 0.0
cO2_0 = 0.0
v = V_Start
nH2O2_0 = cH2O2_0 * v



abbruch_bedingung.terminal = True
abbruch_bedingung.direction = -1

# === Lösung ===
t_span = (0, 7000)
t_eval = np.linspace(t_span[0], t_span[1], 1000)
y0 = [cH2O2_0, cH2O_0, cO2_0]

sol = solve_ivp(
    reaktionssystem, t_span, y0,
    t_eval=t_eval,
    events=abbruch_bedingung
)

# === Auswertung ===
time = sol.t
cH2O2, cH2O, cO2 = sol.y
nH2O2 = cH2O2 * v
nH2O = cH2O * v
nO2 = cO2 * v
UH2O2 = (nH2O2_0 - nH2O2) / nH2O2_0
T = T_Start + dTad * UH2O2

# === JSON für Diagramm erstellen ===
def generateReactionData():
    data = {
        "data_1": {
            "labels": time.tolist(),
            "datasets": [
                {
                    "label": "n(H2O2)",
                    "data": nH2O2.tolist(),
                    "borderColor": "#66c2a5",
                    "backgroundColor": "#66c2a5",
                    "tension": 0.1
                },
                {
                    "label": "n(H2O)",
                    "data": nH2O.tolist(),
                    "borderColor": "#fc8d62",
                    "backgroundColor": "#fc8d62",
                    "tension": 0.1
                },
                {
                    "label": "n(O2)",
                    "data": nO2.tolist(),
                    "borderColor": "#8da0cb",
                    "backgroundColor": "#8da0cb",
                    "tension": 0.1
                }
            ]
        },
        "data_2": {
            "labels": time.tolist(),
            "datasets": [
                {
                    "label": "Temperatur [°C]",
                    "data": T.tolist(),
                    "borderColor": "#e78ac3",
                    "backgroundColor": "#e78ac3",
                    "tension": 0.1
                }
               
            ]
        },
        "data_3": {
            "labels": time.tolist(),
            "datasets": [
                 {
                    "label": "Umsatz H2O2",
                    "data": UH2O2.tolist(),
                    "borderColor": "#FFD700",
                    "backgroundColor": "#FFD700",
                    "tension": 0.1
                }
            ]
        }
    }
    return data
# === JSON speichern ===
with open('./src/Tasks/Reakt/Reaktdata.json', 'w') as output:
    json.dump(generateReactionData(), output, indent=2)

print(" JSON-Datei erfolgreich erstellt: ./src/Tasks/Reakt/Reaktdata.json")

# === Status ===
if sol.status == 1:
    print(f" Abbruch bei t = {sol.t_events[0][0]:.2f} h - Umsatz 95 % erreicht.")
else:
    print("Simulation lief bis zur maximalen Zeit.")
