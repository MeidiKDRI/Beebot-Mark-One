import re
import random
import string
import pandas as pd
import datetime
import requests

#Import pour l'analyse des sentiments
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

user_name = ''

# Quitter
quit_user = r"au revoir|quitter|ciao|hasta la vista|à \+"
quit_bot = ['Au revoir', 'Bye', 'Salut', 'A bientôt']

# Listing fonctions du bot
fct_user = r"fonctionnalités"
fct_bot = ['Je peux répondre à quelques civilités', 'Je donne la météo', 'Je réponds à vos questions']

# Salutations
hi_user = r'salut.*|bonjour.*salut|yo.*'
hi_bot = ['Bonjour', 'Salut', 'Hey bienvenue']

# Comment ça va vous 2 ?
howis_user = r'.*ça va.*|.*tu vas.*|.*vas.*tu.*'
howis_bot = ['oui', 'super', 'nickel']

# Nom du bot      comment tu t'appelles
botname_user = r".*ton nom?| .*tu.*t'appelles?| .*t'appelles.*"
botname_bot = [
      "Beebot Cowboy !",
      "Je suis Beebot mec !",
      "Mon nom est Beebot",
      "Si je te le dis je devrais t'éliminer..."]

# Age
botage_user = r".*age as.*|.*as .* age"
botage_bot = ["On ne pose pas cette question à une dame ^^", "Devine !", "l'age, c'est surfait !"]

# Chanson
song_user = r".*ta (chanson|musique) préférée|.*écoutes quoi.*|.*tu aimes .* musique"
song_bot = [
      "Celle-ci >>> https://www.youtube.com/watch?v=2mbdEWCdnTc",
      "J'aime bien celle-la >>> https://www.youtube.com/watch?v=NIIO8zdDRpY"]

# Module météo
meteo = r"quel temps .* à .*?|.*météo à .*?"

# Lieu
place_user = r'.* habites? .*|.* vis? .*'

# Que fais-tu
doin_user = r'.* fais? .*'
doin_bot = ["Je passe le temps en comptant les 0 et les 1..", "J'exauce 3 voeux si tu frottes ton ordi !", "Je réponds aux questions que tu me poses, c'est pourtant évident !"]

# Horloge
time_user = r".* heure .* est.*| .*heure est.*"

# Incompréhension
misunderstood = ['Whaaaat ?', 'No entiendo le Frenchy', 'Répétez svp']

isawake = True
print("""Bonjour, je suis votre assistant personnel persque intelligent!
      Pour quitter, dîtes moi au revoir.
      Pour connaitres mes fonctions, dites : 'que sais-tu faire' ou 'fonctionnalités'
      Je vous écoute. Quelle est votre question ?""")

while isawake == True :
      
      user_input = input('user : ').lower()

      # Quitter
      if re.search(quit_user, user_input) :
            print('Beebot : ', random.choice(quit_bot))
            isawake = False
      
      # Fonctionnalités du bot
      elif re.fullmatch(fct_user, user_input) :
            print('beebot : ', fct_bot)
      
      # Salutations
      elif re.fullmatch(hi_user, user_input) :
            # Suivant l'heure de la journée
            CurrentHour = int(datetime.datetime.now().hour)
            if CurrentHour >= 6 and CurrentHour < 18:
                  print('Beebot : Bonjour !')
            elif CurrentHour >= 18 and CurrentHour != 6:
                  print('Beebot : Bonsoir !')
            
      # Nom du bot
      elif re.search(botname_user, user_input) :
            print(f'Beebot : {random.choice(botname_bot)}, et toi ?')
            user_name = input('user : ').upper()
            print(f'Beebot : Enchanté {user_name} !')

      # la forme ?
      elif re.search(howis_user, user_input) :
            print(f'Beebot : {random.choice(howis_bot)}, et toi')
            user_howis = input('user :').lower()
            txtblob = TextBlob(user_howis).sentiment.polarity
            if txtblob > 0.00 :
                  print(f'Beebot : Yeaah {user_name} !!! ça fait du bien de voir des gens avec le sourire !!!')
            elif txtblob < 0.00 :
                  print(f"Beebot : Courage {user_name}, plus que 34 785 heures de confinement et c'est terminado...")
            else :
                  print(f"Beebot : Resaisis-toi {user_name} ! ça aurait puêtre pire ! Tu aurais pu être coincé sous le clavier...")

      # Age
      elif re.search(botage_user, user_input) :
            print('Beebot :', random.choice(botage_bot))

      # Chanson
      elif re.search(song_user, user_input) :
            user_input = re.sub(f"[{string.punctuation}]", " ", user_input)
            print('Beebot :', random.choice(song_bot))
            
      # Module Météo
      elif re.fullmatch(meteo, user_input) :
            user_input = re.sub(f"[{string.punctuation}]", " ", user_input)
            # On récupère la ville renseigné par user
            ville = user_input.split()[-1]
            # On fait une requête
            apiUrl =f'http://api.openweathermap.org/data/2.5/weather?q={ville}&appid=9bd0bf7e50511cb6c26d63fa01107896&units=metric&lang=fr'
            wheather = requests.get(apiUrl)
            dataMeteo = wheather.json()
            temp = dataMeteo['main']['temp']
            temps = dataMeteo['weather'][0]['description']
            print(f'Beebot : Il fait {temp} degrés à {ville}')
            print(f'Beebot : Temps {temps}')

      elif re.search(place_user, user_input) :
            user_input = re.sub(f"[{string.punctuation}]", " ", user_input)
            # On récupère l'ip de user
            ip_request = requests.get('https://get.geojs.io/v1/ip.json')
            user_ip = ip_request.json()['ip']
            # On s'en sert pour retourner la ville et le pays du user
            # Puisque le bot est dans sa machine ^^
            geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + user_ip + '.json'
            geo_request = requests.get(geo_request_url)
            geo_data = geo_request.json()
            city = geo_data['city']
            country = geo_data['country']
            print(f'Beebot : Je suis à {city}, en {country}')

      elif re.search(doin_user, user_input) :
            user_input = re.sub(f"[{string.punctuation}]", " ", user_input)
            print(f'Beebot : {random.choice(doin_bot)}')

      elif re.search(time_user, user_input) :
            user_input = re.sub(f"[{string.punctuation}]", " ", user_input)
            H = pd.datetime.now().hour
            Mn = pd.datetime.now().minute
            heure = str(H) + ' heures et ' + str(Mn) + ' minutes'
            print('Beebot : Il est ' + heure)

      else :
            print('Beebot : ', random.choice(misunderstood) )