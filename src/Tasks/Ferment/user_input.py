import numpy as np
from array import array


# initialisieren der Variablen aus Modell-Shet
def get_user_input(prompt, value_range, phases):
    inputs = []  # Eine Liste, um die Eingaben für die Variable zu speichern
    for phase in range(1, phases+1):
        while True:
            try:
                user_input = float(input(f"{prompt}{phase} ({phase}/{phases}): "))
                if value_range[0] <= user_input <= value_range[1] or user_input == 0:
                    inputs.append(user_input)
                    break
                else:
                    print("Bitte geben Sie einen Wert im Bereich von {} bis {} ein.".format(value_range[0], value_range[1]))
            except ValueError:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")
    return np.array(inputs, dtype=float)   # Konvertiere die Liste der Eingaben in Float-Werte und gib sie zurück
