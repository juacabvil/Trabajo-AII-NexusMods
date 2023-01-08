#encoding:utf-8
from app.models import Game,Mod,Colection
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import re
from pprint import pp

from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)

import os, ssl
import time
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def populate():
    extraer_juegos()


def extraer_juegos():

    driver.get("https://www.nexusmods.com/games")
    more_buttons = driver.find_element(By.CLASS_NAME, "js-expand-games")
    driver.execute_script("arguments[0].click();", more_buttons)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    games = soup.find_all("div", class_="tile-desc image-tile-bg")
    for game in games:
        gamename = game.find("p", class_="tile-name").text.strip()
        data = game.find("div", class_="tile-data")
        text = data.text.replace('\n',' ')
        juego = text.split()
        nMods = numberConv(juego[0])
        nDownloads = numberConv(juego[1])
        Game.objects.create(name = gamename, mods = nMods, downloads = nDownloads)

def extraer_mods():
    pass

        

def numberConv(num):
    if 'k' in num:
        return float(num.replace('k', '')) * 1000
    if 'M' in num:
        return float(num.replace('M', '')) * 1000000
    if 'bn' in num:
        return float(num.replace('bn', '')) * 1000000000
    else:
        return float(num)


