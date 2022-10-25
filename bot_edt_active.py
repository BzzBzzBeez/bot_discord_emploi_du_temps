import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920,1080")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all(), description = "Bot Emploi du Temps v1.1")

def saveEdtPicture(nbWeek):
        s=Service('/home/user/folder/chromedriver')
        driver = webdriver.Chrome(options=chrome_options, service=s)
        start_url = "https://formations.cci-paris-idf.fr/IntNum/index.php"
        driver.get(start_url)

        ids_file = open("/home/user/folder/ids_file.txt","r")
        content = ids_file.read()
        content_list = content.split(":")
        ids_file.close()

        id_co = content_list[0]
        pass_co = content_list[1]

        fieldId = driver.find_element(By.NAME,"login")
        fieldId.send_keys(id_co)
        fieldPass = driver.find_element(By.NAME,"password")
        fieldPass.send_keys(pass_co + Keys.ENTER)

        time.sleep(.75)
        driver.get("https://formations.cci-paris-idf.fr/IntNum/index.php/apprenant/planning/courant/")

        for nb in range(nbWeek):
                arrowBtn = driver.find_element(By.XPATH,'/html/body/main/div[1]/div/div[2]/div[1]/a[2]').click()
                time.sleep(.75)

        fieldPlanning = driver.find_element(By.CLASS_NAME,"planning")
        fieldPlanning.screenshot("/home/user/folder/planning.png")

        driver.quit()

        return nbWeek


@bot.event
async def on_message(message):
        channel = bot.get_channel(INSERT_CHANNEL_CODE_ID)
        if message.content.startswith("/edt"):
                now = datetime.now()
                now_strf = now.strftime("%d/%m/%Y %H:%M:%S")
                print("/edt : ", now_strf)

                if message.content == "/edt" or message.content == "/edt 0":
                        saveEdtPicture(0)
                        await message.channel.send("Emploi du temps posté : <#INSERT_CHANNEL_CODE_ID>")
                        await channel.send("Voici l'**Emploi du temps** de la semaine **courante** :", file=discord.File('/home/user/folder/planning.png'))
                        return #Leave if no parameters

                number = int(message.content.split()[1])
                if number <= 6 and number >=0 :
                        nbWeek = saveEdtPicture(number)
                        if nbWeek == 1:
                                await channel.send("Voici l'**Emploi du temps** de la semaine **prochaine** :", file=discord.File('/home/user/folder/planning.png'))
                        elif nbWeek == 2:
                                await channel.send("Voici l'**Emploi du temps** dans **2 semaines** :", file=discord.File('/home/user/folder/planning.png'))
                        elif nbWeek == 3:
                                await channel.send("Voici l'**Emploi du temps** dans **3 semaines** :", file=discord.File('/home/user/folder/planning.png'))
                        elif nbWeek == 4:
                                await channel.send("Voici l'**Emploi du temps** dans **4 semaines** :", file=discord.File('/home/user/folder/planning.png'))
                        elif nbWeek == 5:
                                await channel.send("Voici l'**Emploi du temps** dans **5 semaines** :", file=discord.File('/home/user/folder/planning.png'))
                        elif nbWeek == 6:
                                await channel.send("Voici l'**Emploi du temps** dans **6 semaines** :", file=discord.File('/home/user/folder/planning.png'))
                        await message.channel.send("Emploi du temps posté : <#INSERT_CHANNEL_CODE_ID>")
                else:
                        message.channel.send("Le paramètre à besoin d'être : `x <= 6` et `x >= 0` !")

        elif message.content.startswith("/help"):
                now = datetime.now()
                now_strf = now.strftime("%d/%m/%Y %H:%M:%S")
                print("/help : ", now_strf)

                await message.channel.send("Tapez `/edt` pour afficher **l'emploi du temps**\nTapez `/edt 1-6`, pour les semaines suivantes (max 6)\nEx : `/edt 1` = l'emploi du temps de la semaine prochaine `/edt 2` = l'emploi du temps dans 2 semaines.\n*La commande peut prendre jusqu'à 10 secondes pour s'afficher.*")

print("\n--------------------")
print("EDT v1.1")
now = datetime.now()
now_strf = now.strftime("%d/%m/%Y %H:%M:%S")
print("Initialized : ", now_strf)

bot.run("INSERT_BOT_KEY")
