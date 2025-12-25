import json

import json

def feedback_schatzung():
    # Lade Loesung aus der JSON-Datei
    with open('src/Tasks/FermentExercises/parameter_loesung.json', 'r') as loesung_file:
        loesung = json.load(loesung_file)
    
    # Lade Schaetzung aus der JSON-Datei
    with open('src/Tasks/Ferment/nutzer_eingaben.json', 'r') as schatzung_file:
        schatzung = json.load(schatzung_file)
    
    # Initialisiere ein Dictionary fuer das Feedback
    feedback = {"Feedback": {}}

    # Vergleiche die Schaetzungen mit den Loesungen fuer jede Phase
    for param in loesung:  # Iteration ueber Parameter (z. B. "Feed", "Zuluft")
        if isinstance(loesung[param], dict):
            if param not in feedback["Feedback"]:
                feedback["Feedback"][param] = {}  # Initialisierung des Parameters im Feedback
            
            for phase in loesung[param]:  # Iteration ueber die Phasen (Phase_0, Phase_1, ...)
                phase_feedback = {
                    "status": "",
                    "message": ""
                }
                
                print(f"Vergleich fuer {param} - {phase}:")

                # Loesung und Schaetzung abrufen
                phase_loesung = loesung[param][phase]
                phase_schatzung = schatzung.get(param, {}).get(phase)  # Verhindert KeyError
                
                if phase_schatzung is None:
                    phase_feedback["status"] = "Fehler"
                    phase_feedback["message"] = f"Keine Schaetzung fuer {param} - {phase} gefunden!"
                    print(phase_feedback["message"])
                    feedback["Feedback"][param][f"{param}-{phase}"] = phase_feedback
                    continue
            
                # Besondere Behandlung fuer den Fall, dass die Loesung 0 ist
                if phase_loesung == 0:
                    if phase_schatzung == 0:
                        phase_feedback["status"] = "Erfolgreich"
                        phase_feedback["message"] = f"Deine Schaetzung fuer {param} - {phase} ist korrekt (beide sind 0)."
                    else:
                        phase_feedback["status"] = "Falsch"
                        phase_feedback["message"] = f"Deine Schaetzung fuer {param} - {phase} ist nicht korrekt. Versuche es noch einmal."
                    print(phase_feedback["message"])
                    feedback["Feedback"][param][f"{param}-{phase}"] = phase_feedback
                    continue
            
                # Berechne die relative Differenz, wenn die Loesung nicht null ist
                differenz = abs(phase_schatzung - phase_loesung)
                relative_differenz = (differenz / abs(phase_loesung)) * 100
            
                # Bestimme, wie nah die Schaetzung an der Loesung ist
                if relative_differenz <= 20:
                    phase_feedback["status"] = "Erfolgreich"
                    phase_feedback["message"] = f"Deine Schaetzung von {phase_schatzung} fuer {param} - {phase} ist nahe genug an der Loesung."
                elif 20 < relative_differenz <= 50:
                    phase_feedback["status"] = "Fast"
                    phase_feedback["message"] = f"Du bist nah dran! Deine Schaetzung von {phase_schatzung} fuer {param} - {phase} ist entfernt von der Loesung."
                elif 50 < relative_differenz <= 100:
                    phase_feedback["status"] = "Entfernt"
                    phase_feedback["message"] = f"Versuche es noch einmal! Deine Schaetzung von {phase_schatzung} fuer {param} - {phase} ist weit entfernt von der Loesung."
                else:
                    if phase_schatzung < phase_loesung:
                        phase_feedback["status"] = "Zu niedrig"
                        phase_feedback["message"] = f"Du musst hoeher schaetzen! Deine Schaetzung von {phase_schatzung} fuer {param} - {phase} ist mehr als 100% entfernt."
                    else:
                        phase_feedback["status"] = "Zu hoch"
                        phase_feedback["message"] = f"Du musst niedriger schaetzen! Deine Schaetzung von {phase_schatzung} fuer {param} - {phase} ist mehr als 100% entfernt."
                
                print(phase_feedback["message"])
                feedback["Feedback"][param][f"{param}-{phase}"] = phase_feedback
                
        if isinstance(loesung[param], (int, float)):  # Falls es eine Zahl oder Zahl-String ist
            phase_loesung = float(loesung[param])
            phase_feedback = {
                "status": "",
                "message": ""
            }

            # Loesung und Schaetzung abrufen
            phase_loesung = float(loesung[param])
            phase_schatzung = float(schatzung[param]) # Verhindert KeyError
            
            if phase_schatzung is None:
                phase_feedback["status"] = "Fehler"
                phase_feedback["message"] = f"Keine Schaetzung fuer {param} gefunden!"
                print(phase_feedback["message"])
                feedback["Feedback"][param] = phase_feedback
                continue
        
            # Besondere Behandlung fuer den Fall, dass die Loesung 0 ist
            if phase_loesung == 0:
                if phase_schatzung == 0:
                    phase_feedback["status"] = "Erfolgreich"
                    phase_feedback["message"] = f"Deine Schaetzung fuer {param} ist korrekt (beide sind 0)."
                else:
                    phase_feedback["status"] = "Falsch"
                    phase_feedback["message"] = f"Deine Schaetzung fuer {param} ist nicht korrekt. Versuche es noch einmal."
                print(phase_feedback["message"])
                feedback["Feedback"][param] = phase_feedback
                continue
        
            # Berechne die relative Differenz, wenn die Loesung nicht null ist
            differenz = abs(phase_schatzung - phase_loesung)
            relative_differenz = (differenz / abs(phase_loesung)) * 100
        
            # Bestimme, wie nah die Schaetzung an der Loesung ist
            if relative_differenz <= 20:
                phase_feedback["status"] = "Erfolgreich"
                phase_feedback["message"] = f"Deine Schaetzung von {phase_schatzung} fuer {param}  ist nahe genug an der Loesung."
            elif 20 < relative_differenz <= 50:
                phase_feedback["status"] = "Fast"
                phase_feedback["message"] = f"Du bist nah dran! Deine Schaetzung von {phase_schatzung} fuer {param}  ist entfernt von der Loesung."
            elif 50 < relative_differenz <= 100:
                phase_feedback["status"] = "Entfernt"
                phase_feedback["message"] = f"Versuche es noch einmal! Deine Schaetzung von {phase_schatzung} fuer {param}  ist weit entfernt von der Loesung."
            else:
                if phase_schatzung < phase_loesung:
                    phase_feedback["status"] = "Zu niedrig"
                    phase_feedback["message"] = f"Du musst hoeher schaetzen! Deine Schaetzung von {phase_schatzung} fuer {param}  ist mehr als 100% entfernt."
                else:
                    phase_feedback["status"] = "Zu hoch"
                    phase_feedback["message"] = f"Du musst niedriger schaetzen! Deine Schaetzung von {phase_schatzung} fuer {param}  ist mehr als 100% entfernt."
            
            print(phase_feedback["message"])
            feedback["Feedback"][param] = phase_feedback

    # Speichere das Feedback in einer JSON-Datei
    with open('src/Tasks/Ferment/feedback.json', 'w') as feedback_file:
        json.dump(feedback, feedback_file, indent=4, ensure_ascii=False)

# Funktion aufrufen
feedback_schatzung()

