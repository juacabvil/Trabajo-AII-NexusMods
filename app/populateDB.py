#encoding:utf-8
from app.models import Game,Mod,Colection
from bs4 import BeautifulSoup
import datetime 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

    JUEGOS_A_CARGAR = 50
    TIEMPO_ESPERA_COLECTIONS = 1
def populate():
    return extraer_juegos()
     


def extraer_juegos():
    Game.objects.all().delete()
    Mod.objects.all().delete()
    Colection.objects.all().delete()
    driver.get("https://www.nexusmods.com/games")
    more_buttons = driver.find_element(By.CLASS_NAME, "js-expand-games")
    driver.execute_script("arguments[0].click();", more_buttons)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    games = soup.find_all("a", class_="mod-image", href=True)
    for gametag in games[:JUEGOS_A_CARGAR]:
        #creacion juego
        gamename = gametag.find("p", class_="tile-name").text.strip()
        print(gamename)
        data = gametag.find("div", class_="tile-data")
        text = data.text.replace('\n',' ')
        juego = text.split()
        nMods = numberConv(juego[0])
        nDownloads = numberConv(juego[1])
        gameObject = Game.objects.create(name = gamename, mods = nMods, downloads = nDownloads)
        #Ir a página top mods por juego
        enlace = 'https://www.nexusmods.com/'+ gametag['href']+'/mods/top/'
        driver.get(enlace)
        page_source = driver.page_source
        soup2 = BeautifulSoup(page_source, 'lxml')
        mods = soup2.find_all("li", class_="mod-tile")
        for mod in mods:
            modname = mod.find("p",class_="tile-name").text.strip()
            last_update = mod.find("time", class_="date").text.replace("Uploaded: ","").strip()
            modlast_update_parsed = datetime.datetime.strptime(last_update, '%d %b %Y')
            moduploader = mod.find("div", class_="author").text.replace("Uploader: ","").strip()
            moddescription = mod.find("p", class_="desc").text.strip()
            modlikes = numberConv(mod.find("li", class_="endorsecount inline-flex").find("span","flex-label").text)
            modcategory = mod.find("div", class_="category").text.strip() 
            game = gameObject
            Mod.objects.create(name = modname, last_update = modlast_update_parsed, uploader = moduploader, description = moddescription, likes = modlikes, category = modcategory, game = game)
            
        #Ir a colecciones
        enlace = 'https://next.nexusmods.com'+ gametag['href'] + '/collections?adultContent=0&page=1&sortBy=latest_published_revision_rating'
        driver.get(enlace)
        try:
            wait = WebDriverWait(driver, TIEMPO_ESPERA_COLECTIONS)
            espera = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.nx-tile__bottom-layout')))
        except:
            print('espera superada')
            continue
        elemento = driver.find_elements(By.CSS_SELECTOR, '.nx-tile__bottom-layout')
        if(len(elemento)>1):
            page_source = driver.page_source
            soup3 = BeautifulSoup(page_source, 'lxml')
            colections = soup3.find_all("div", class_="nx-tile__bottom-layout")
            for colection in colections:
                colectionName = colection.find("p", class_="nx-type-body nx-tile__title").text.strip()
                statswrapper = colection.find("div", class_="nx-tile__stats-rating-wrapper")
                stats = statswrapper.find_all("span", class_="nx-tile-stat__value")
                colectionDownloads = numberConv(stats[0].text.strip())
                colectionLikes = numberConv(stats[1].text.strip())
                colectionmods = numberConv(colection.find("div", class_="nx-tile__mod-count-layout").text.strip())
                Colection.objects.create(name=colectionName, downloads = colectionDownloads, likes = colectionLikes, mods=colectionmods, game = gameObject)
        else:
            print('espera superada')

    return True     

def numberConv(num):
    if 'k' in num:
        return float(num.replace('k', '')) * 1000
    if 'M' in num:
        return float(num.replace('M', '')) * 1000000
    if 'bn' in num:
        return float(num.replace('bn', '')) * 1000000000
    else:
        return float(num)


