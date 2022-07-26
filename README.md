# Candilib_Robot
Script automatique permettant de réserver une place sur la plateforme du permis de conduire candilib

Je n'encourage pas l'utilistation de robots sur la plateforme candilib, ce script est avant tout à but instructif.
Je ne me porte pas responsable des conséquences de l'utilisation de ce script.

___________________________________________________

<h2>Prérequis :</h2>
 
<h3>Librairies :</h3>
 
   _pip install selenium
 
   _pip install opencv-python
 
   _pip install pytesseract ( Sous Windows, besoin de telecharger son installer : https://github.com/UB-Mannheim/tesseract/wiki)
  
  _Télécharger chromedriver : https://chromedriver.chromium.org/
  
 <h2>Configuration</h2>
    
   <h4>bot.py :</h4>
    
   Ligne 14 : Entrer le chemin absolue du fichier .exe pytesseract.
    
   Ligne 20   Entrer chemin absolue du fichier .exe chromedriver.
    
   <h4>config.py</h4>
    
   Ligne 4,5,6 : Correspond à la valeur transmise à la fonction sleep(), il s'agit du temps de pause en seconde entre chaque actions sur l'application nécessitant un chargement de la page.
    
   Ligne 19 : Coller le lien de connexion dans la variable log_link
    
   Ligne 20 : Dans la variable dict_dep sont référencés les departements qui seront traités pour la recherche de   
              place. La valeur pour chaque departement est son chemin XPATH sous Google Chrome. Ajouter ou supprimer des lignes en fonction de vos préférences. 
    
   Ligne 29 :  Dans la variable matrix_dep_centre sont référencés les centres qui seront traités pour la recherche de   
              place. L'ordre défini pour les départements doit être le même que pour dict_dep. La valeur pour chaque centre est son chemin XPATH sous Google Chrome. Ajoutez ou supprimez des lignes en fonction de vos préférences.
___________________________________________________

<h2>Utilisation :</h2>
