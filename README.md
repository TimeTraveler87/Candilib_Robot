# Candilib_Robot
Script automatique permettant de réserver une place sur la plateforme du permis de conduire candilib

Je n'encourage pas l'utilistation de robots sur la plateforme officiel de candilib, ce script est avant tout à but instructif.
Je ne me porte pas responsable des sanctions que la plateforme pourrait prendre à votre encontre en conséquence de l'utilisation de ce script.

___________________________________________________

<h1>Prérequis :</h1>
 _Python3
 
 _Google chrome
<h3>Librairies :</h3>

    pip install selenium
    pip install opencv-python
    pip install pytesseract
<h4>Sous Windows :</h4>
 
 Besoin de telecharger l'installer pour pytesseract : https://github.com/UB-Mannheim/tesseract/wiki et de préciser le path du fichier .exe (voir Configuration)
  
  _Télécharger chromedriver : https://chromedriver.chromium.org/ et préciser le path du .exe (voir Configuration)
  
<h4>Sous Debian/Ubuntu/Linux Mint :</h4>

    sudo apt install sox

<h4>Sous Mac :</h4>

    sudo port install sox
  
 <h1>Configuration</h1>
    
   <h3>bot.py :</h3>
    
   Ligne 15 : Entrer le chemin absolue du fichier .exe pytesseract.
    
   Ligne 24 : Entrer chemin absolue du fichier .exe chromedriver.
   
   Ligne 28 : Après chaque tour infructueux, le programme s'interrompt pendant X à Y secondes
   
   <h4>Sous Mac/Linux/Ubuntu/Linux Mint :</h4>
   
   Ligne 250 : Intégrer l'instruction en enlevant le signe "#" à la ligne 
   
   Ligne 249 : Effacer la ligne d'instruction
    
   <h3>config.py :</h3>
    
   Ligne 4,5,6 : Correspond à la valeur transmise à la fonction sleep(), il s'agit du temps de pause en seconde entre chaque actions sur l'application nécessitant un chargement de la page.
    
   Ligne 19 : Coller le lien de connexion dans la variable log_link
    
   Ligne 20 : Dans la variable dict_dep sont référencés les departements qui seront traités pour la recherche de   
              place. La valeur pour chaque departement est son chemin XPATH sous Google Chrome. Ajouter ou supprimer des lignes en fonction de vos préférences. 
    
   Ligne 29 :  Dans la variable matrix_dep_centre sont référencés les centres qui seront traités pour la recherche de   
              place. L'ordre défini pour les départements doit être le même que pour dict_dep. La valeur pour chaque centre est son chemin XPATH sous Google Chrome. Ajoutez ou supprimez des lignes en fonction de vos préférences.
___________________________________________________

<h1>Utilisation :</h1>
<h3>Sur le terminal, lancez ces commandes successives pour démarrer le programme :</h3>

    python -i .\bot.py
    >>> Bot()
Vous pouvez laisser tourner le programme en fond et faire autre chose sur votre machine.

<h3>/!\IMPORTANT/!\</h3>
Le programme peut en théorie résoudre le captcha nécessaire à la réservation d'une place, cependant s'il échoue vous serez avertit par un bip sonore qui vous avertira que le programme a selectionné une date et un horaire, mais qu'il est incapable de résoudre le captcha. Dans ce cas, ce sera a vous de résoudre manuellement le captcha pour confirmer votre place.
