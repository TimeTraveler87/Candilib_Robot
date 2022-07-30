from datetime import date
from time import sleep
#tts_ : temps de pause entre chaque actions sur l'application nécessitant un chargement de la page
tts_accueil = 2 #Limite testé 1.2 
tts_pageload = 1 #Limite testé 0.5
tts_notpageload = 0.5 #Limite testé 0.2
dict_month = {1:'//*[@id="tab-janvier"]/div/div/div/div/div', 2:'//*[@id="tab-février"]/div/div/div/div/div'
, 3:'//*[@id="tab-mars"]/div/div/div/div/div', 4:'//*[@id="tab-avril"]/div/div/div/div/div', 5:'//*[@id="tab-mai"]/div/div/div/div/div'
,  6:'//*[@id="tab-juin"]/div/div/div/div/div', 7:'//*[@id="tab-juillet"]/div/div/div/div/div', 8:'//*[@id="tab-août"]/div/div/div/div/div'
, 9:'//*[@id="tab-septembre"]/div/div/div/div/div', 10:'//*[@id="tab-octobre"]/div/div/div/div/div', 11:'//*[@id="tab-novembre"]/div/div/div/div/div'
, 12:'//*[@id="tab-décembre"]/div/div/div/div/div'}
l_month = list(dict_month.values())
l_month_keys = list(dict_month.keys())
month = int(date.today().month) #mois actuel du système
l_month = l_month[month-1:month+3] #liste des xpath de tous les mois réservables

log_link = ''#Entrez le lien candilib
dict_dep = {77:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[5]/div',
             78:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[6]/div', 
             91:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[7]/div', 
             92:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[8]/div', 
             93:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[9]/div', 
             94:'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[10]/div'}
list_keys_dep =list(dict_dep.keys())
matrix_dep_centre=[ #77
                    {'AVON':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div',
                     'MELUN':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[6]/div/div'
                     },
                     #78
                     {'VELIZY VILLACOUBLAY':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[7]/div/div'
                     },
                     #91
                     {'EVRY':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[3]/div/div',
                      'MASSY':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[4]/div/div',
                      'MONTGERON':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[5]/div/div',
                      'VILLABE':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[6]/div/div'
                     },
                     #92
                     {'ANTONY':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div',
                      'CLAMART':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[3]/div/div',
                      'GENNEVILLIERS':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[4]/div/div',
                     },
                     #93
                     {'NOISY LE GRAND':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[3]/div/div',
                      'ROSNY SOUS BOIS':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[4]/div/div'
                     },
                    #94
                    {'RUNGIS':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div',
                     'MAISONS ALFORT':'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div[4]/div/div'  
                    }
                  ]
list_dep_xpath = list(dict_dep.values())#dict_dep
CAPTCHA_IMAGES = {
    "L'avion": "airplane",
    "Les ballons": "balloons",
    "L'appareil photo": "camera",
    "L‘appareil photo": "camera",
    "La Voiture": "car",
    "Le chat": "cat",
    "La chaise": "chair",
    "Le trombone": "clip",
    "L'horloge": "clock",
    "Le nuage": "cloud",
    "L'ordinateur": "computer",
    "‘ordinateur": "computer",
    "L'enveloppe": "envelope",
    "L'oeil": "eye",
    "Le drapeau": "flag",
    "Le dossier": "folder",
    "Le pied": "foot",
    "Le graphique": "graph",
    "La maison": "house",
    "La clef": "key",
    "Laclef":"key",
    "La feuille": "leaf",
    "L'ampoule": "light-bulb",
    "Le cadenas": "lock",
    "La loupe": "magnifying-glass",
    "L'homme": "man",
    "La note de musique": "music-note",
    "Le pantalon": "pants",
    "Le crayon": "pencil",
    "L'imprimante": "printer",
    "Le robot": "robot",
    "Les ciseaux": "scissors",
    "Les lunettes de soleil": "sunglasses",
    "L'étiquette": "tag",
    "L'ètiquette": "tag",
    "L'arbre": "tree",
    "Le camion": "truck",
    "Le T-Shirt": "t-shirt",
    "Le parapluie": "umbrella",
    "La femme": "woman",
    "La planète": "world",
    "La planéte": "world",
}
