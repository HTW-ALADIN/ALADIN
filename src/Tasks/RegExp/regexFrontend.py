import tkinter as tk
import regexBackend as rb
import random
import string
import json
import sys

# Globale Variablen für Widgets und Buttons
entry_widgets = []
label_widgets = []
regexListAllRows = None
regexListAllColumns = None

# Hilfsfunktion zur Erzeugung eines zufälligen Großbuchstabens
def create_random_letter():
    return random.choice(string.ascii_uppercase)

# Hilfsfunktion zur Erzeugung einer Zufallszahl
def create_random_number(): 
    return random.randint(0, 9)

# Funktion zum Erstellen eines Textfeldes (Entry)
def create_entry(root, text, row, column):
    entry = tk.Entry(root, width=30, justify="center")
    entry.insert(0, text)
    entry.grid(row=row, column=column, ipady=30)
    return entry

# Funktion zum Erstellen eines Labels für die Regex-Anzeige
def create_regex_label(root, text, row, column):
    label = tk.Label(root, text=text, width=25, height=2)
    label.grid(row=row, column=column)
    label_widgets.append(label)

# Funktion zum Abrufen des Inhalts einer Zeile
def get_row_content(root, row):
    row_content = []
    for widget in root.grid_slaves(row=row):
        if isinstance(widget, tk.Entry):
            row_content.append(widget.get())

    row_content.reverse()
    row_content_string = ''.join(row_content)
    return row_content_string

# Funktion zum Abrufen des Inhalts einer Spalte
def get_column_content(root, column):
    column_content = []
    for widget in root.grid_slaves(column=column):
        if isinstance(widget, tk.Entry):
            column_content.append(widget.get())

    column_content.reverse()
    column_content_string = ''.join(column_content)
    return column_content_string

# Funktion zur Erstellung eines Rasters von zufälligen Buchstaben und Zahlen
def create_grid(root, rows, columns, seed):
    rowseed = generate_and_initialize_seeds(seed, rows)
    columnseed = generate_and_initialize_seeds(seed + rows, columns)
    entry_widgets = []
    for i in range(1, rows + 1):
        row_entries = []
        for j in range(1, columns + 1):
            roll = random.random()
            if roll < 0.25:
                entry = create_entry(root, create_random_number(), i, j)
            else:
                entry = create_entry(root, create_random_letter(), i, j)
            
            row_entries.append(entry)
        entry_widgets.append(row_entries)
    return entry_widgets

# Funktion zur Generierung und Initialisierung von Zufallszahlen
def generate_and_initialize_seeds(central_seed, num_seeds):
    random.seed(central_seed)
    seeds = [random.randint(1, 1000) for _ in range(num_seeds)]  
    return seeds

# Funktion zur Setzung des Zufallszahlengenerators
def set_seed(seed):
    random.seed(seed)

# Funktion zum Erstellen und Initialisieren des Rasters und der Regex-Anzeigen
def create_and_initialize_grid():
    global entry_widgets
    global label_widgets

    for row in entry_widgets:
        for entry in row:
            entry.destroy()

    for label in label_widgets:
        label.destroy()

    entry_widgets = create_grid(root, rows, columns, seed)
    regexListAllColumns, regexListAllRows = [], []
    label_widgets = []
    row_seed = generate_and_initialize_seeds(seed, rows)
    column_seed = generate_and_initialize_seeds(seed + rows, columns)
    for i in range(1, rows + 1):
        set_seed(row_seed[i - 1])
        row_content_string = get_row_content(root, i)
        generated_regex, regexListRow = rb.generate_random_regex(row_content_string)
        create_regex_label(root, generated_regex, i, 0)
        regexListAllRows.append(regexListRow)

    for j in range(1, columns + 1):
        set_seed(column_seed[j - 1])
        column_content_string = get_column_content(root, j)
        generated_regex, regexListColumn = rb.generate_random_regex(column_content_string)
        create_regex_label(root, generated_regex, 0, j)
        regexListAllColumns.append(regexListColumn)

    return entry_widgets, regexListAllRows, regexListAllColumns

# Funktion zur Formatierung der Regex-Listen
def format_regexList(regexListAllColumns, regexListAllRows):
    regexLabelColumns = [''.join(sublist) for sublist in regexListAllColumns]
    regexLabelRows = [''.join(sublist) for sublist in regexListAllRows]
    return regexLabelColumns, regexLabelRows

# Funktion zum Entfernen aller Widgets
def remove_all_widgets(widget):
    for widget in widget.winfo_children():
        widget.destroy()

# Funktion zum Starten aller Widgets
def start_all():
    remove_all_widgets(root)
    entry_widgets, regexListAllRows, regexListAllColumns = create_and_initialize_grid()
    return regexListAllRows, regexListAllColumns
    
# Funktion zum Abrufen der Regex-Listen
def get_regex_lists():
    return regexListAllRows, regexListAllColumns  

# Hauptfunktion des Programms
def main(Datacolumns,Datarows,userseed ):
    global rows, columns, seed
    global regexListAllColumns, regexListAllRows
    rows=Datarows
    columns=Datacolumns
    seed = userseed
    global root
    root = tk.Tk()
    regexListAllRows, regexListAllColumns=start_all()
    regexLabelColumns, regexLabelRows = format_regexList(regexListAllColumns, regexListAllRows)

    validationmatrix = [[None for _ in range(columns)] for _ in range(rows)]
    with open("src/Tasks/RegExp/JSONFiles/userData.json", "w") as f:
        json.dump(validationmatrix, f)
          
    
    with open("src/Tasks/RegExp/JSONFiles/validationmatrix.json", "w") as f:
        json.dump(validationmatrix, f)
        
    with open('src/Tasks/RegExp/JSONFiles/regex_lists.json', 'w') as file:
        json.dump({'rows': regexListAllRows, 'columns': regexListAllColumns}, file)    
    
    with open("src/Tasks/RegExp/JSONFiles/labels.json", "w") as f:
        json.dump({"RowLabel":regexLabelRows, "ColumnLabel":regexLabelColumns}, f)
     
    return json.dumps({"RowLabel":regexLabelRows, "ColumnLabel":regexLabelColumns})
        
if __name__ == "__main__":
   
        columns = int(sys.argv[1])
        rows = int(sys.argv[2])
        seed = int(sys.argv[3])
        
        main(columns, rows, seed)