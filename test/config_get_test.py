# -*- coding: utf-8 -*-
# Created at 24/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
# Third Party Imports
import requests
from bs4 import BeautifulSoup
# Local Application Imports

with open("config.mcsm", "r") as config_file:
    settings = config_file.readlines()

    # Ignores any "#" or "//" starting lines or any empty strings in the lines.
filtered_settings = [setting.strip() for setting in settings
                     if not setting.startswith("#")
                     and not setting.startswith("//")
                     and setting.strip() != ""]

settings_dictionary = dict()
for setting in filtered_settings:
    key_value_setting = setting.split("=")
    settings_dictionary[key_value_setting[0].strip()] = key_value_setting[-1].strip()

print(settings_dictionary)