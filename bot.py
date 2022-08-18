import base64
from random import randint
import winsound,os
import cv2
import io
from pytesseract import pytesseract
from PIL import Image,ImageChops
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
from config import log_link,list_keys_dep, matrix_dep_centre, l_month,tts_pageload,tts_notpageload,tts_accueil, list_dep_xpath, month, CAPTCHA_IMAGES
from time import sleep
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
pytesseract.tesseract_cmd = r''#Chemin absolue de pytesseract.exe
from selenium.common.exceptions import NoSuchElementException
#Règle générale : return 1 = succès, return 0 = Réponse captcha (faux) , return -1 = collision avec autre candidat, return -3 = aucune place trouvé , return -2 =Error NoSuchElementException
txt_path = 'Tmp_Image/txt.png'
merged_path ='Tmp_Image/merged_obj.png'
merged_clean_path = 'Tmp_Image/merged_clean.png'

class Bot():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'')#Chemin absolue de chromedriver.exe
        sleep(tts_pageload)
        value = -3
        i=0
        while(value == -3 or value == -2):
            print("_____________________NOUVEAU TOUR_______________________")
            if(i>0 and value != -2):
                print('')
                sleep(randint(120,130))
            elif(value == -2):
                self.login()
            value = self.main()
            i+=1
        print("_______________________________________________________")
        print("PLACE RESERVEE AVEC SUCCES")
        print(str(i) + " tour(s)")
        self.driver.quit()
   
    def main(self):
        value = self.page_accueil_dpt()
        return value
        
    def login(self):
        self.driver.get(log_link)
        sleep(tts_accueil)

    def page_accueil_dpt(self):  
        backto_centre_btn_xpath = '//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[4]/button'
        for i in range(0,len(list_dep_xpath)):                                          # Ici on entre dans un département
            dict_centre_dispo=[]
            try : 
                self.driver.find_element(By.XPATH, list_dep_xpath[i])
            except NoSuchElementException:
                return -2
            dep_btn = self.driver.find_element(By.XPATH, list_dep_xpath[i])
            dep_btn.click()
            sleep(tts_pageload)#pageload
            self.print_departement(i)
            
            dict_centre_dispo = self.list_centre_dispo(matrix_dep_centre[i])
            value_centre_dispo = list(dict_centre_dispo.values())
            keys_centre_dispo = list(dict_centre_dispo.keys())
            for j in range(0,len(dict_centre_dispo)):                                  # Ici on entre dans un centre du département de la boucle ci-dessus
                try:
                    self.driver.find_element(By.XPATH,value_centre_dispo[j])
                except NoSuchElementException:
                    return -2
                print("____________________________________________")
                print("Le centre  "+ keys_centre_dispo[j] +" est disponible" )
                centre_btn = self.driver.find_element(By.XPATH,value_centre_dispo[j])
                centre_btn.click()
                sleep(tts_pageload)#pageload
                value = self.page_selection_date() # Renvoi -1 si collision dans ce cas on se trouve dans l'interface de selection de mois et d'horaire du centre en question
                if(value==1):# On arrete le code avec return si une place est réservé
                    return True
                elif(j+1<len(dict_centre_dispo)):# ACTION DE RETOUR SI IL NE S'AGIT PAS DU DERNIER CENTRE, SINON ACCUEIL
                    back_btn = self.driver.find_element(By.XPATH,backto_centre_btn_xpath)
                    back_btn.click()
                    sleep(tts_pageload)#pageload
            #POUR SELECTION DEPARTEMENT UNIQUEMENT --> Besoin de recharger la page plutôt que de faire un retour sinon le chemin xpath change
            self.login()
        return -3
      
    def page_selection_date(self):
        l_horaire=['initialisation']
        result = -3
        for i in range(0,len(l_month)):# check si dates dispo pour le mois en question
            mois_select = self.mois_select_to_string(i)
            print("____________________________________________")
            print(mois_select)
            try:
                self.driver.find_element(By.XPATH,l_month[i])
            except Exception:
                print("     Pas de dates pour le mois de "+mois_select)
            else:
                for j in range(0,10):
                    try:#On cherche la date suivante à commencer par la dernière 
                        self.driver.find_element(By.XPATH,'//*[@id="tab-'+mois_select+'"]/div/div/div/div['+str(j+1)+']/div')
                    except Exception:
                        print("Limite à "+str(j)+ " date(s)")
                        break
                    else:
                        #On rentre dans le sous-menu de cette date pour accéder à ses horaires  
                        btn_date = self.driver.find_element(By.XPATH,'//*[@id="tab-'+mois_select+'"]/div/div/div/div['+str(j+1)+']/div')
                        btn_date.click()
                        l_horaire = self.list_horaire_dispo(mois_select,(j+1))
                        while(len(l_horaire)!=0):
                            i=0
                            l_horaire = self.get_into_horaire(l_horaire) #En paramètre : la liste des horaires , Renvoi une liste vide si le programme est rentré dans la page suivante
                            if(len(l_horaire)==0):#Si le programme n'a pas rencontré un message de collision (cas selection horaire)
                                sleep(tts_pageload)#pageload                   
                                self.confirm_step()
                                result = self.captcha_bypass(False)
                                while(result==0 and i<3):#3 essaies pour le captcha
                                    result = self.captcha_bypass(True)
                                    i=i+1
                                if(result==-1):
                                    sleep(tts_notpageload)
                                    l_horaire = self.list_horaire_dispo(mois_select,(j+1))
                        return result
            finally: # A SAVOIR Finally s'execute dans tous les cas, malgré les return plus haut # A PARTIR D'ICI : on passe au mois suivant sachant qu'il y en a 4 à tester dans tous les cas
                if(i<3 and (len(l_horaire)!=0) and result!=1):
                    try:
                        self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div/div[2]/div/a['+str(i+2)+']')
                    except Exception:
                        print("Erreur fonction interfaces_post_centre dans le finally -> Incohérence avec la condition if(i<3) : Problème récurrent lorsque le chargement de la page n'a pas le temps de se faire (Il faut augmenter le temps de time_to_sleep)")
                    else:
                        btn_mois_suivant = self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div/div[2]/div/a['+str(i+2)+']')
                        sleep(tts_notpageload)
                        btn_mois_suivant.click()
        return  0

    def confirm_step(self):
        #checkbox 1
        sleep(tts_notpageload)
        self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[1]/div/div[1]/div').click()
        #checkbox 2
        sleep(tts_notpageload)
        self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[2]/div/div[1]/div').click()
        sleep(tts_notpageload)
        #Bouton confirm "JE NE SUIS PAS UN ROBOT" qui mène à l'anti-robot
        self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div/div/button/span').click()
        sleep(tts_accueil)#chargement long du captcha

    def get_into_horaire(self,l_horaire):
        sleep(tts_notpageload)#not pageload
        for i in range(len(l_horaire)-1,-1,-1):
            try:
                l_horaire[i].click()
            except Exception:
                print('Erreur try l_horaire.click()')
            finally:
                sleep(tts_pageload)#pageload
                error_msg = self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div')                     
                if(error_msg.is_displayed()):#Si il y a message d'erreur
                    close_error = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[1]/button')
                    close_error.click()
                else:
                    return []   
        return print('fail boucle get_into_horaire')

    def list_horaire_dispo(self,mois_string,num_div_date):
        l_horaire = []
        #print("_____________________________________________________")
        #print("         Date à la position "+str(num_div_date))
        for i in range(17):# car 16 horaires possibles pour une journée, 16+1 pour entrer dans l'except qui ira break
            try:
                self.driver.find_element(By.XPATH,'//*[@id="tab-'+ mois_string +'"]/div/div/div/div['+ str(num_div_date) +']/div[2]/div/button['+str(i+1)+']')
            except Exception:
                print("         "+str(i)+" horaires disponibles")
                break
            else:
                l_horaire.append(self.driver.find_element(By.XPATH,'//*[@id="tab-'+ mois_string +'"]/div/div/div/div['+ str(num_div_date) +']/div[2]/div/button['+str(i+1)+']'))
        return l_horaire
    
    def mois_select_to_string(self,compteur):
        mois_string = ''
        valeur_mois = month+compteur
        if(valeur_mois==1):
            mois_string='janvier'
        elif(valeur_mois==2):
            mois_string='février'
        elif(valeur_mois==3):
            mois_string='mars'
        elif(valeur_mois==4):
            mois_string='avril'
        elif(valeur_mois==5):
            mois_string='mai'
        elif(valeur_mois==6):
            mois_string='juin'
        elif(valeur_mois==7):
            mois_string='juillet'
        elif(valeur_mois==8):
            mois_string='août'
        elif(valeur_mois==9):
            mois_string='septembre'
        elif(valeur_mois==10):
            mois_string='octobre'
        elif(valeur_mois==11):
            mois_string='novembre'
        elif(valeur_mois==12):
            mois_string='décembre'
        return mois_string

    def list_centre_dispo(self,dict_centre):
    # On ajoute les centres qui proposent une place à une liste l_centre_dispo que l'on retourne
        new_dict_centre = {}
        keys_centre = list(dict_centre.keys())
        value_centre = list(dict_centre.values())
        for i in range(0,len(value_centre)):
            tmp_xpath = value_centre[i]+'/span'
            try:
                self.driver.find_element(By.XPATH,tmp_xpath)
            except Exception:#Cas : centre est disponible
                new_dict_centre.update({keys_centre[i]:value_centre[i]})
        return new_dict_centre

    def print_departement(self,compteur):#Fonction pour faciliter le débogage
        value_dep = list_keys_dep[compteur]
        print("____________________________________________")
        print("DEPARTEMENT : "+ str(value_dep))

    def captcha_bypass(self,retry):#Retour -1 -> Collision , retour 0 -> Réponse invalide , retour 1 -> Success
            value = -1
            if(retry):
                self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div/div/button').click()
                sleep(tts_accueil)# CAPCTCHA chargement
            if(self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div/div/div').is_displayed() == False):#SI SOUS MENU CAPTCHA NE S'AFFICHE PAS -> FREEZE JE NE SUIS PAS UN ROBOT
                #Retour à la page selection horaire
                self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[2]/button[1]').click()
                sleep(tts_pageload)
                return value
            #Texte de la description objet captcha
            url_txt = self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div/div/div/div[4]/div[1]/img').get_attribute('src')
            txt_img = self.desc_object_process(url_txt)
            txt_img = str(txt_img.rstrip())
            txt_img = txt_img.lstrip()
            #Cas d'erreur pour l'étiquette
            if(txt_img==''):
                txt_img = "L'étiquette"
            #print("     "+txt_img)
            aim_clean_path = "captcha_clean/"+CAPTCHA_IMAGES[txt_img]+".png"
            #Image des objets captcha
            url_obj = self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div/div/div/div[4]/div[3]/img').get_attribute('src')
            re_shape = self.object_process(url_obj)
            if(re_shape==-1):
                bytes = self.get_file_content_chrome(url_obj)
                if(bytes == -2):
                    winsound.Beep(650,1500)
                    #os.system('play -nq -t alsa synth {} sine {}'.format(650, 1500))
                    sleep(60*3)
                    return value
                imageStream = io.BytesIO(bytes)
                img_merged = Image.open(imageStream)
                img_merged.save(merged_path)
            #Rend l'image en texte = noir fond = blanc
                merged_clean = self.imagecolor_traitement(merged_path)
                merged_clean.save(merged_clean_path)
            #Rend l'image ref en texte = noir fond = blanc
            img_aim = self.imagecolor_traitement("captcha_images/"+CAPTCHA_IMAGES[txt_img]+".png")
            img_aim.save(aim_clean_path)
            self.image_split(merged_clean_path)
            sol_number = self.compare_image(aim_clean_path)
            #Clique sur la case réponse, puis sur le bouton confirmer
            self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div/div/div/div[4]/div[4]/button['+str(sol_number)+']').click()
            sleep(tts_pageload)#not pageload
            self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[2]/button[2]').click()
            sleep(tts_pageload)#notpageload
            try:
                self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div')
            except Exception:
                print("CONFIRMATION REUSSIE")
            else:
                if(self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div').is_displayed()):
                    text = self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div/div[1]').get_attribute('textContent')
                    if("Réponse invalide" in text):
                        #Fermer la pop up
                        self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div/div[1]/button').click()
                        value = 0
                    elif(("Dépassement de la limite" in text) or ("Il n'y a pas de place pour ce créneau" in text)):
                        value=-1
                        #Fermer la pop up
                        self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div/div[1]/button').click()
                        #Retour à la page selection horaire
                        self.driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/div/div/div/div[2]/div/form/div[2]/button[1]').click() 
                        sleep(tts_pageload)#pageload
                    else:
                        value = 1
            finally:
                return value

    def image_split(self,file_path):
        im = Image.open(file_path)
        w,h = im.size
        for i in range(1,7):
            if(i==1):
                r=w/3.68
                l=0
                b=h/3-h/31
                t=0
            elif(i==2):
                r= (w/2) + (0.58)*(w/4)
                l=1.4*(w/4) 
                t=0
                b=h/3-h/31
            elif(i==3):
                r= w
                l=w*0.65
                t=0
                b=h/3-h/31
            elif(i==4):
                r= w/3.68
                l=0 
                t=h/2+h/22
                b=h - h/7.2
            elif(i==5):
                r= (w/2) + (0.58)*(w/4)
                l=1.4*(w/4)
                t=h/2+h/22
                b=h - h/7.2
            elif(i==6):
                r= w 
                l=w*0.65
                t=h/2+h/22
                b=h - h/7.2
            new_img = im.crop((l,t,r,b))
            new_img.resize((32,32))
            new_img.save("Tmp_Image/split_"+str(i)+".png")

    def orb_sim(self,img1, img2):
        orb = cv2.ORB_create(fastThreshold=0,edgeThreshold=0)
        # detect keypoints and descriptors
        kp_a, desc_a = orb.detectAndCompute(img1, None)
        kp_b, desc_b = orb.detectAndCompute(img2, None)
        # define the bruteforce matcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) 
        #perform matches
        matches = bf.match(desc_a, desc_b)
        #Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between
        similar_regions = [i for i in matches if i.distance < 50]  
        if len(matches) == 0:
            return 0
        return len(similar_regions) / len(matches)

    def compare_image(self,ref_path):
        im_ref = cv2.imread(ref_path, 0)
        list =[[],[]]
        for i in range(1,7):
            path = "Tmp_Image/split_"+str(i)+".png"
            im = Image.open(path)
            im_test = cv2.imread(path, 0)
            orb_similarity = self.orb_sim(im_ref, im_test)  #1.0 means identical. Lower = not similar
            if(len(list[0])!=0):
                if(len(list[0])==1):
                    list[0].append(orb_similarity)
                    list[1].append(i)
                if(list[0][0]>=list[0][1]):
                    del list[0][1]
                    del list[1][1]
                else:
                    del list[0][0]
                    del list[1][0]
            else:
                list[0].append(orb_similarity)
                list[1].append(i)                          
            #print("            For image "+str(i)+" similarity using ORB is: ", orb_similarity)
        return list[1][0]

    def object_process(self,url):
        try:
            urllib.request.urlretrieve(url, "obj.png")
        except Exception:
            return -1
        else:
            img = self.imagecolor_traitement("obj.png")
            img.save(merged_clean_path)
            return 0

    def desc_object_process(self,url):
        urllib.request.urlretrieve(url, "txt.png")
        img = self.imagecolor_traitement("txt.png")
        img.save(txt_path)
        txt = pytesseract.image_to_string(txt_path)
        return txt
    
    def imagecolor_traitement(self,file_path):# renvoi l'imgae avec fond = blanc , texte = noir
        img = Image.open(file_path)
        alpha = img.split()[-1]
        alpha_inv = ImageChops.invert(alpha)
        return alpha_inv

    def get_file_content_chrome(self, uri):
        result = self.driver.execute_async_script("""
            var uri = arguments[0];
            var callback = arguments[1];
            var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
            var xhr = new XMLHttpRequest();
            xhr.responseType = 'arraybuffer';
            xhr.onload = function(){ callback(toBase64(xhr.response)) };
            xhr.onerror = function(){ callback(xhr.status) };
            xhr.open('GET', uri);
            xhr.send();
            """, uri)
        if type(result) == int :
            return -2
        return base64.b64decode(result)
