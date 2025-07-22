import sys
import eel
import time
import xlwings as xw
import datetime
import os
from query import query_to_get_gmr, query_to_get_og_ni, query_get_operation_intervention, query_get_equipes_pilotes, query_get_id_og_from_numero_og, query_get_id_og_from_numero_ni, query_get_equipes_intervenantes
from query_utils import make_query, get_headers
from function_utils import get_background_color, get_operation_day_number, days_in_year, getColumn,is_operation_valid, isEquipeHere

##Récupération des requetes
exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0,f"{exe_dir}\\_internal\\query.py")

eel.init("web")


##FONCTIONS LIEES A JS
#Récupération des identifiants de l'utilisateur
@eel.expose
def get_data(nni, mdp):
    global headers
    headers, response_tuple = get_headers(nni, mdp)
    if (headers is None):
        nni, mdp = "", ""
        eel.display_error(response_tuple)
    else:
        eel.go_to('./pages/filters.html')
    return

#Récupération des GMR de la DB
@eel.expose
def get_gmr():
    query = query_to_get_gmr()
    result = make_query(query,headers)
    li_gmr = []
    for gmr in result:
        li_gmr.append(gmr['GMR'])
    eel.display_gmr(li_gmr)

#Récupération des og et ni dans la db selon la date de debut, de fin, et le gmr choisi
@eel.expose
def get_filters(gmr, date_start, date_end):
    global og
    global ni
    global main_gmr
    main_gmr = gmr
    start = time.time()
    query = query_to_get_og_ni(date_end, date_start, gmr)
    og_ni = make_query(query,headers)
    og = []
    ni = []

    list_operation_with_GMR = []
    for i in range(len(og_ni)):
        if og_ni[i]["NUMERO_OG"] not in list_operation_with_GMR and og_ni[i]["LIBELLE"] == gmr :
            list_operation_with_GMR.append(og_ni[i]["NUMERO_OG"])


    dic_operations_unique = {}
    for i in range(len(og_ni)):
        if og_ni[i]["NUMERO_OG"] in list_operation_with_GMR :
            if og_ni[i]["NUMERO_OG"] not in dic_operations_unique:
                dic_operations_unique[og_ni[i]["NUMERO_OG"]] = []
            dic_operations_unique[og_ni[i]["NUMERO_OG"]].append(og_ni[i])

    for operation_globale in dic_operations_unique:

        query = query_get_equipes_intervenantes(dic_operations_unique[operation_globale][0]['NUMERO_NI'])
        list_equipe = make_query(query,headers)

        if is_operation_valid(dic_operations_unique[operation_globale], list_equipe):

            detail = ""
            statut = dic_operations_unique[operation_globale][0]['STATUT_NI']
            color_map = {
                'Diffusée': 'blue',
                'Sans Objet': 'lightgray',
                'En construction': 'orange',
                'Validée': 'green'
            }
            color = color_map.get(statut, 'black')
            detail = f"<p style='color:{color}; padding-left:8px;'> {statut} </p>"

            og.append(f"{dic_operations_unique[operation_globale][0]['NUMERO_OG']} {detail}")
            ni.append(f"{dic_operations_unique[operation_globale][0]['NUMERO_NI']} {detail}")

    end = time.time()
    print(f"traitement de {len(og_ni)} en {end - start} secondes")

    eel.go_to('./OG_choice.html')

@eel.expose
def get_og():
    return eel.add_og_to_selection(og)

@eel.expose
def get_ni():
    return eel.add_ni_to_selection(ni)

@eel.expose
def go_back():
    eel.go_back('./filters.html')

@eel.expose
def generate_excel(operation):
    operation = operation.split()[0]
    start = time.time()
    isOG = "OG" in operation
    isNI = "NI" in operation
    eel.step("récupération des données en cours")
    if (not isOG and not isNI):
        return
    elif (isOG):
        id_og = make_query(query_get_id_og_from_numero_og(operation), headers)[0]['ID_OG']
    elif (isNI):
        id_og = make_query(query_get_id_og_from_numero_ni(operation), headers)[0]['ID_OG']

    query = query_get_operation_intervention(id_og)

    result = make_query(query,headers)
    result_rows = result
    data_row = result_rows[0]

    eel.step("récupération de TEMPLATE.xlsm")

    wb_obj = xw.Book(f"./_internal/TEMPLATE.xlsm")
    sheet = wb_obj.sheets['FicheDeCoordination']

    eel.step("modification du fichier excel")

    #Titre de la fiche
    sheet['A1'].value = f"Fiche De Coordination {data_row["NUMERO_NI"]}"

    #Information En-Tete

    adr = data_row["ADR"]
    for i in range(1,len(result)):
        print(result[i]["ADR"])
        if result[i]["ADR"] not in adr :
            adr = adr + " - " + result[i]["ADR"]
            print(adr)

    sheet['S4'].value = adr
    sheet['I4'].value = data_row["NUMERO_OG"]
    sheet['C4'].value = data_row["NUMERO_NI"]
    sheet['AM4'].value = f"INDICE : {data_row['NUMERO_INDICE']}"

    #Date de debut / semaine de debut
    start_date_split = data_row["DATE_DEB_NI"][slice(0, 10)].split("-")
    start_date = datetime.datetime(int(start_date_split[0]), int(start_date_split[1]),int(start_date_split[2]))
    sheet['D9'].value = start_date
    sheet['D10'].value = int(start_date.strftime("%W"))+1

    #Date de fin / semaine de fin
    end_date_split = data_row["DATE_FIN_NI"][slice(0, 10)].split("-")
    end_date = datetime.datetime(int(end_date_split[0]), int(end_date_split[1]),int(end_date_split[2]))
    sheet['K9'].value = end_date
    sheet['K10'].value = int(end_date.strftime("%W"))+1

    ## CHANGER POUR JOUR CALENDRIER
    #année en cours + jour de l'année (x/365) pour calendrier
    sheet['AT7'].value = start_date.strftime("%Y")
    sheet['AT9'].value = start_date.strftime("%j")

    #Création de la liste des équipes pilotes
    query = query_get_equipes_pilotes(main_gmr)
    equipes_pilotes = make_query(query, headers) or []
    query = query_get_equipes_intervenantes(data_row["NUMERO_NI"])
    equipes_intervenantes = make_query(query, headers) or []

    for i, equipe in enumerate(equipes_pilotes + equipes_intervenantes):
        sheet[f'AQ{i+1}'].value = equipe['CODE']

    #Début du calendrier des opérations
    index = 19
    correct_i_value_for_excel = 0 #Pitie faut trouver mieux mais la c'est pas facile facile
    operation_global_start_day_number = int(start_date.strftime("%j"))

    for i in range(len(result_rows)):

        nom_equipe_code = ""

        if i != len(result_rows) :
            if "LIAISON" in result_rows[i]['ADR']:
                if i+1 < len(result_rows) and result_rows[i]['ID_OU'] == result_rows[i+1]['ID_OU']:
                    correct_i_value_for_excel += 1
                    continue
                else :
                    if isEquipeHere(result_rows[i]):
                        nom_equipe_code = result_rows[i]['NOM'] + " - " + result_rows[i-1]['CODE_TB17'] + " - " + result_rows[i]['CODE_TB17']
            elif isEquipeHere(result_rows[i]):
                nom_equipe_code = result_rows[i]['NOM'] + " - " + result_rows[i]['CODE_TB17']

        localisation = result_rows[i]['ADR']
        libelle_ou = result_rows[i]['LIBELLE_OU']

        sheet[f'A{index + (i - correct_i_value_for_excel)*2}'].value = localisation
        sheet[f'D{index + (i - correct_i_value_for_excel)*2}'].value = nom_equipe_code
        sheet[f'AM{index + (i - correct_i_value_for_excel)*2}'].value = libelle_ou

        operation_start_day_number = int(get_operation_day_number(result_rows[i]['DATE_DEB_NI']))
        operation_end_day_number = int(get_operation_day_number(result_rows[i]['DATE_FIN_NI']))

        if operation_end_day_number < operation_start_day_number:
            operation_end_day_number += days_in_year(int(start_date.strftime("%Y")))

        background_color = (255, 255, 255)
        if(result_rows[i].get('CODE_TB17')):
            background_color = get_background_color(result_rows[i].get('CODE_TB17'), sheet)

        first_day_operation = operation_start_day_number-operation_global_start_day_number
        last_day_operation = operation_end_day_number-operation_global_start_day_number+1

        for j in range(first_day_operation,last_day_operation,1):
            if j < 0:
                continue
            if getColumn(j) == 'AM':
                break
            sheet[f'{getColumn(j)}{index + (i - correct_i_value_for_excel)*2}'].color = background_color
            sheet[f'{getColumn(j)}{index + (i - correct_i_value_for_excel)*2+1}'].color = background_color

    eel.step("definition nom du fichier")
    if not os.path.exists("ficheExcel"):
        os.makedirs("ficheExcel")

    adr_filename = data_row["ADR"]
    for char in '<>?[]:|/':
        adr_filename =  adr_filename.replace(char, '_')
    sheet['AT10'].value = adr_filename

    file_name = f"ficheExcel/FC_{data_row['NUMERO_NI']}_S{start_date.strftime('%W')}_S{end_date.strftime('%W')}_{adr_filename}_V0.xlsm"

    file_name = file_name.replace(" ", "_")

    eel.step("sauvegarde du fichier")
    wb_obj.save(file_name)

    end = time.time()
    print(f"{end - start}s d'execution gen de la fiche")

eel.start("./index.html", size=(315, 535), mode='default')




#                                              ++++++++
#                                        ++++++++++++++++++++
#                                    ++++++++++++++++++++++++++++
#                                  ++++++++++++++++++++++++++++++++
#                                ++++++++++++++++++++++++++++++++++++
#                              ++++++++++++++++++++++++++++++++++++++++
#                             ++++++++++++++++++++++++++++++++++++++++++
#                            ++++++++++++++++++++++++++++++++++++++++++++
#                           ++++++++++++++++++++++++++++++++++++++++++++++
#                          ++++++++++=====+++++++++++++++++++++++++++++++++
#                          +++++++++:      .:=+++++++++++++++++++++++++++++
#                         ++++++++++: -++++-..++++-:+++++++-:::-=+++++++++++
#                         ++++++++++: -+++++: -+++. =++++: .:--. .=+++++++++
#                         ++++++++++: -++++-..++++. =+++- :+++++- .+++++++++
#                         ++++++++++:                             .+++++++++
#                         ++++++++++: -++++. :++++. =+++: :+++++++++++++++++
#                         ++++++++++: -+++++: .+++. =+++=. :=+++++++++++++++
#                         ++++++++++- -++++++- .++-.  :+++-:.     -+++++++++
#                          +++++++++++++++++++=++++++=+++++++=====+++++++++
#                          ++++++++++++++++++++++++++++++++++++++++++++++++
#                           ++++++++++++++++++++++++++++++++++++++++++++++
#                            ++++++++++++++++++++++++++++++++++++++++++++
#                             ++++++++++++++++++++++++++++++++++++++++++
#                              ++++++++++++++++++++++++++++++++++++++++
#                                ++++++++++++++++++++++++++++++++++++
#                                  ++++++++++++++++++++++++++++++++
#                                    ++++++++++++++++++++++++++++
#                                        ++++++++++++++++++++
#                                              +++++++++