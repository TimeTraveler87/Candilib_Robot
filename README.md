# Candilib_Robot
Script automatique permettant de réserver une place sur la plateforme du permis de conduire candilib

Je n'encourage pas l'utilistation de robots sur la plateforme officiel de candilib, ce script est avant tout à but instructif.
Je ne me porte pas responsable des sanctions que la plateforme pourrait prendre à votre encontre en conséquence de l'utilisation de ce script.

___________________________________________________

<h1>Prérequis :</h1>
 _Python3
 
 _Google chrome
<h3>Librairies :</h3>
 
   _pip install selenium
 
   _pip install opencv-python
 
   _pip install pytesseract, Sous Windows, besoin de telecharger son installer : https://github.com/UB-Mannheim/tesseract/wiki et de préciser le path du .exe (voir Configuration)
  
  _Télécharger chromedriver : https://chromedriver.chromium.org/ et préciser le path du .exe (voir Configuration)
  
 <h1>Configuration</h1>
    
   <h3>bot.py :</h3>
    
   Ligne 14 : Entrer le chemin absolue du fichier .exe pytesseract.
    
   Ligne 20 : Entrer chemin absolue du fichier .exe chromedriver.
   
   Ligne 28 : Après chaque tour infructueux, le programme s'interrompt pendant X à Y secondes
    
   <h3>config.py :</h3>
    
   Ligne 4,5,6 : Correspond à la valeur transmise à la fonction sleep(), il s'agit du temps de pause en seconde entre chaque actions sur l'application nécessitant un chargement de la page.
    
   Ligne 19 : Coller le lien de connexion dans la variable log_link
    
   Ligne 20 : Dans la variable dict_dep sont référencés les departements qui seront traités pour la recherche de   
              place. La valeur pour chaque departement est son chemin XPATH sous Google Chrome. Ajouter ou supprimer des lignes en fonction de vos préférences. 
    
   Ligne 29 :  Dans la variable matrix_dep_centre sont référencés les centres qui seront traités pour la recherche de   
              place. L'ordre défini pour les départements doit être le même que pour dict_dep. La valeur pour chaque centre est son chemin XPATH sous Google Chrome. Ajoutez ou supprimez des lignes en fonction de vos préférences.
___________________________________________________

<h1>Utilisation :</h1>
<h3>Sur le terminal :</h3>

    python -i .\bot.py
    >>> Bot()

