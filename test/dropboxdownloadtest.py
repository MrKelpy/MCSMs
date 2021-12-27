# -*- coding: utf-8 -*-
# Created at 26/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
# Third Party Imports
import requests
from bs4 import BeautifulSoup

# Local Application Imports

data = requests.get("https://www.dropbox.com/home/MCSMs/Forge/1.16.5")
soup = BeautifulSoup(data.text, "html.parser")

for i in soup.find_all("href"):
    print(i)
