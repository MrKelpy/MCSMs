# -*- coding: utf-8 -*-
# Created at 24/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
# Third Party Imports
# Local Application Imports

with open("config.mcsm", "r") as config_file:
    settings = config_file.readlines()

filtered_settings = [setting.strip() for setting in settings
                     if not setting.startswith("#")
                     and not setting.startswith("//")
                     and setting.strip() != ""]

print(filtered_settings)