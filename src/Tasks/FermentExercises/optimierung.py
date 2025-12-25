import optuna
import numpy as np
from scipy.integrate import solve_ivp
from differentialgleichung import ODE_Bioreactor_Monod
from numbers import Number

def get_max_value(parameter, sol):
    match parameter.lower():
        case "cx":
            return np.max(sol.y[0]) 
        case "cp":
            return np.max(sol.y[3])
        case "cs1":
            return np.max(sol.y[1]) 
        case "cs2":
            return np.max(sol.y[2]) 
        case "c_ox":
            return np.max(sol.y[4]) 
        case "c_o2_out":
            return np.max(sol.y[5]) 
        case "c_co2_out":
            return np.max(sol.y[6]) 
        case _:
            return None  # Statt False, um None-Check durchzuführen


def get_min_value(parameter, sol):
    match parameter.lower():
        case "cx":
            return np.min(sol.y[0]) 
        case "cp":
            return np.min(sol.y[3])
        case "cs1":
            return np.min(sol.y[1]) 
        case "cs2":
            return np.min(sol.y[2]) 
        case "c_ox":
            return np.min(sol.y[4]) 
        case "c_o2_out":
            return np.min(sol.y[5]) 
        case "c_co2_out":
            return np.min(sol.y[6]) 
        case _:
            return None  # Statt False, um None-Check durchzuführen

def objective(trial, t_start, t_end, y0, consts, t_span, varierendeParameter, maxParameter, minParameter):
    #maxParameter   : Parameter zu maximieren
    #minParameter   : Parameter zu minimieren
    #varierendeParameter    :   Liste von Parametern mit Bereich, der bei dem Maximierungsprozess bzw Minimierungsprozess berücksichtigt werden
    try:
        # Liste der Parameter, die du überprüft werden
        parameter_namen = ['Feed', 'Zuluft', 'Cs1', 'Cs2', 'C_ox', 'C_o2_out', 'C_Co2_out']

        # Schleife, um durch die Parameter zu iterieren
        for param in parameter_namen:
            if param in varierendeParameter:
                param_min = varierendeParameter[param]['min']
                param_max = varierendeParameter[param]['max']
                
                # Dynamischer Name für den Parameter in suggest_uniform
                param_value = trial.suggest_uniform(param.lower(), param_min, param_max)
                
                # Falls der Parameter "Feed" ist, speichere den Wert in consts[19]
                if param.lower() == 'feed':
                    consts[19] = param_value
                elif param.lower() == 'zuluft':
                    consts[3] = param_value
                '''elif param.lower() == 'bolusc':  
                    consts[19] = param_value    #! an welcher Stelle bei consts liegt bolusC????
                elif param.lower() == 'bolousn': #! consts ist ein übergebende Parameter "const_array_array" in der Funktion berechnung in berechnungen.py
                    consts[19] = param_value       #! const_array_array ist die Rückgabe der Funktion berechnung_der_Tabelle1 in berechnungen.py
                elif param.lower() == 'drehzahl':
                    consts[19] = param_value
                elif param.lower() == 'druck':
                    consts[19] = param_value
                elif param.lower() == 'dauer':
                    consts[19] = param_value'''

        # Lösung des ODE-Systems
        sol = solve_ivp(ODE_Bioreactor_Monod, [t_start, t_end], y0, args=(consts,), t_eval=t_span)

        # Initialisierung der Werte
        max_value = float('-inf')
        min_value = float('inf')

        if maxParameter:
            check = get_max_value(maxParameter, sol)
            if check is not None:
                max_value = check

        if minParameter:
            check = get_max_value(minParameter, sol)
            if check is not None:
                min_value = check
        
        cs =  y0[1]

        if maxParameter and minParameter:
            # Falls keine Werte ermittelt werden konnten
            if max_value == float('-inf') or min_value == float('inf'):
                print("Warnung: Kein gültiger Wert für maxParameter oder minParameter gefunden.")
                return float('nan')
            # Ziel: Maximiere max_value und minimiere min_value
            objective_value = min_value - max_value   # Maximierung von max_value und Minimierung von min_value
        elif maxParameter and not minParameter:
            if max_value == float('-inf'):
                print("Warnung: Kein gültiger Wert für maxParameter oder minParameter gefunden.")
                return float('nan')
            objective_value = max_value   # Maximierung von max_value
        else :
            check = get_min_value(minParameter, sol)
            if check is not None:
                min_value = check
            if min_value == float('inf'):
                print("Warnung: Kein gültiger Wert für maxParameter oder minParameter gefunden.")
                return float('nan')
            objective_value = min_value    # Minimierung von min_value

        if sol.success:
            trial.set_user_attr("sol", sol)  
            trial.set_user_attr("cs", cs)

        return objective_value

    except Exception as e:
        print(f"Fehler in der Optimierung: {e}")
        return float('nan')
