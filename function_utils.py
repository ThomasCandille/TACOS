import datetime

def get_background_color(code, sheet):
    color_mapping = {
        "STAIA": ("AS7", (61, 112, 172)),
        "STGP": ("AS9", (249, 115, 133)),
        "STEL": ("AS10", (111, 118, 123)),
        "STEC": ("AS11", (184, 159, 211)),
        "STEPP": ("AS13", (221, 223, 224))
    }
    
    for key, value in color_mapping.items():
        if key in code:
            sheet[value[0]].value = True
            return value[1]
    
    return (255, 255, 255)

def get_operation_day_number(operation_date):
    operation_start = operation_date[slice(0, 10)].split("-")
    operation_start_datetime = datetime.datetime(int(operation_start[0]), int(operation_start[1]),int(operation_start[2]))
    operation_start_day_number = operation_start_datetime.strftime("%j")
    return operation_start_day_number

def days_in_year(year):
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year + 1, 1, 1)
    return (end_date - start_date).days

def getColumn(index) :
    ascii_of_A = 65
    ascii_of_H = 72
    ascii_of_Z = 90
    ascii_value = ascii_of_H + index
    if ascii_value > ascii_of_Z :
        ascii_second_letter = (ascii_value%ascii_of_Z)-1
        return "A" + chr(ascii_of_A + ascii_second_letter)
    return chr(ascii_value)

def get_element_of_operation(operations):
    returned_NOM_list = []
    returned_TYPE_list = []
    for ou in operations:
        returned_NOM_list.append(ou["NOM"])
        returned_TYPE_list.append(ou["TYPE"])
    return returned_NOM_list,returned_TYPE_list

def get_occurence_of_element(list_equipe):
    unique_codes = set()
    for element in list_equipe:
        code = element['CODE'] if isinstance(element, dict) else element
        if code is None:
            continue
        unique_codes.add(code)
    return len(unique_codes) > 1

def is_operation_valid(operation,list_equipe):
    list_nom, list_partie_prenante = get_element_of_operation(operation)
    isNotPartiePrenante = list_partie_prenante.count('Societe tierce') == 0
    isMoreThanOne = len(list_partie_prenante) > 1
    isNotAlone = get_occurence_of_element(list_equipe)
    isNotDI = True
    if len(list_nom) > 0:
        for nom in list_nom:
            if nom != None and nom.find("CDI") != -1:
                isNotDI = False
    is_valid = isNotPartiePrenante and isMoreThanOne and isNotAlone and isNotDI
    return is_valid

def isEquipeHere(row):
    if row['NOM'] != None and row['CODE_TB14'] != None :
        return True