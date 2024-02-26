import random
import string
import re

# Funktion zur Erzeugung eines zufälligen Großbuchstabens
def create_random_letter():
    return random.choice(string.ascii_uppercase)


# Funktion zur Generierung eines zufälligen Zeichenbereichs um das gegebene Zeichen
def generate_character_set(char):
    num_chars_before = random.randint(0, 6)  
    num_chars_after = random.randint(0, 6)  

    start_char = chr(max(ord('A'), ord(char) - num_chars_before))
    end_char = chr(min(ord('Z'), ord(char) + num_chars_after + 1))
    
    return f'[{start_char}-{end_char}]'


# Funktion zur Generierung eines gemischten Musters aus Buchstaben und Zahlen
def generate_mixed_pattern():
    letter_range = generate_range()
    number_range = generate_number_range()
    
    return f'[{letter_range}{number_range}]'
    

# Funktion zur Generierung eines negierten Zeichenbereichs um das gegebene Zeichen
def generate_negated_character_set(char):

    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    start_char = create_random_letter()
    end_char = create_random_letter()

    start_index = alphabet.index(start_char)
    end_index = alphabet.index(end_char)
    
    if start_index > end_index:
        start_char, end_char = end_char, start_char    
    
    if start_char <= char <= end_char :
        return generate_negated_character_set(char)
    else:
        return f'[^{start_char}-{end_char}]'


# Funktion zur Generierung eines zufälligen Zeichenbereichs um das gegebene Zeichen
def generate_range(char):
    roll = random.random()
    if roll < 0.25:
        ran = random.choice(string.ascii_uppercase)
        while char == ran:
            ran = random.choice(string.ascii_uppercase)

        roll = random.random()
        if roll <= 0.5:
            return f'({char}|{ran})'  
        return f'({ran}|{char})'  
    elif roll >= 0.25 and roll < 0.50:
        ran0 = random.choice(string.ascii_uppercase)
        ran1 = random.choice(string.ascii_uppercase)
        while ran0 == ran1 or ran0 == char or ran1 == char:
            ran0 = random.choice(string.ascii_uppercase)
            ran1 = random.choice(string.ascii_uppercase)
        result = char + ran0 + ran1
        return f'[{result}]'  
    elif roll >= 0.5 and roll < 0.75:
        excluded_chars = [char]
        list_chars = []

        for _ in range(3):
            random_char = random.choice([c for c in string.ascii_uppercase if c not in excluded_chars])
            list_chars.append(random_char)

        result = f'[^{"".join(list_chars)}]'
        return result
    else:
        return f'[{char}]'


# Funktion zur Generierung eines Zahlenbereichs um die gegebene Zahl
def generate_number_range(number):
    left_distance = random.randint(0, number)
    right_distance = random.randint(0, 9 - number)
    
    start_number = number - left_distance
    end_number = number + right_distance
    return f'[{start_number}-{end_number}]'


# Funktion zur Generierung eines regulären Ausdrucks-Teils mit einem Quantifier
def generate_unary(char):
    op = ""
    roll = random.random()
    if roll < 0.29:
        op = "*"  
    elif roll >= 0.29 and roll < 0.58:
        op = "+"  
    else:
        op = "?"  
    return f'{char}{op}'  


# Funktion zur Generierung eines regulären Ausdrucks-Teils mit dem gleichen Quantifier wie das vorherige Zeichen
def generate_same_unary(char):
    op = ""
    roll = random.random()
    if roll < 0.18:
        return generate_range(char)  
    elif roll >= 0.18 and roll < 0.55:
        op = "+"  
    else:
        op = "*"  
    return f'{char}{op}'  


# Funktion zur Rückgabe eines regulären Ausdrucks-Teils
def getRegexPart(regexPart):
    return regexPart


# Funktion zur Rückgabe einer Liste von regulären Ausdrucks-Teilen
def getRegexList(regexList):
    return regexList


# Funktion zur Generierung eines regulären Ausdrucks für ein gegebenes Wort
def generate_regex(word):
    result = ""
    skip = False
    regexList = []
    
    for i in range(len(word)): 
        if skip:
            skip = False
            continue
        roll = random.random()
        if roll < 0.12:
            regexPart = generate_negated_character_set(word[i])
        else:
            roll = random.random()
            if roll < 0.25:
                if word[i].isnumeric():
                    regexPart=generate_number_range(int(word[i]))                 
                else:     
                    regexPart = generate_character_set(word[i])
            else:
                roll = random.random()
                if roll < 0.3:
                    regexPart = "."

                else:
                    roll = random.random()
                    if roll < 0.4:
                         regexPart = generate_range(word[i])

                    elif roll >= 0.4 and roll < 0.65:
                        regexPart = word[i]

                    else:
                        if i == len(word) - 1:
                            roll = random.random()
                            regexPart = generate_unary(word[i])

                        elif word[i] == word[i + 1]:
                            roll = random.random()
                            regexPart = generate_same_unary(word[i])

                        #skip = True  # Überspringe das nächste Zeichen
                        else:
                            regexPart = generate_range(word[i])
        result += regexPart
        getRegexPart(regexPart)
        regexList.append(regexPart)
        
    if result == word:
        return generate_regex(word)  
    return result, regexList  


# Funktion zum Setzen des Zufallszahlengenerators
def set_seed(seed):
    random.seed(seed)


# Funktion zur Generierung eines zufälligen regulären Ausdrucks für das gegebene Wort
def generate_random_regex(word):
    result, regexList = generate_regex(word)
    return result, regexList


# Funktion zum Überprüfen, ob die Benutzereingabe mit den gegebenen regulären Ausdrücken übereinstimmt
def check_input(user_input, regexRow, regexColumn):
    flags = re.IGNORECASE  
    match_column = re.match(regexColumn, user_input, flags)
    match_row = re.match(regexRow, user_input, flags)
      
    if match_column is not None and match_row is not None:
        if match_column.group() == user_input and match_row.group() == user_input:
            return True  
    return False
