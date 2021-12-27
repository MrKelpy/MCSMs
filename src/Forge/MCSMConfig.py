# -*- coding: utf-8 -*-
# Created at 26/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
import os

# Third Party Imports
import requests
from bs4 import BeautifulSoup

# Local Application Imports
from MCSMLogger import MCSMLogger


class MCSMConfig:
    """
    This class implements a way to retrieve the mcsm settings in the
    config file in a dictionary, ready to be used.
    This class parents MCSMPlayerdataBackups, MCSMServer and MCSMBackups
    """


    def __init__(self, logger: MCSMLogger):
        self.__server_files_path = os.path.join(os.getcwd(), "server_files")
        self.config_path = os.path.join(self.__server_files_path, "config.mcsm")
        self.__logger = logger
        self.__ensure_config_existance()


    def load_settings(self):
        """
        Parses the settings config file into a dictionary to be used in the server run.
        :return:
        """
        with open(self.config_path, "r") as config_file:
            settings = config_file.readlines()

        # Ignores any "#" or "//" starting lines or any empty strings in the lines.
        filtered_settings = [setting.strip() for setting in settings
                             if not setting.startswith("#")
                             and not setting.startswith("//")
                             and setting.strip() != ""]

        # Creates the dictionary by splitting the settings by the "="
        # and assigning the leftmost part to the value, and the rightmost to the key.
        settings_dictionary = dict()
        for setting in filtered_settings:
            key_value_setting = setting.split("=")

            if key_value_setting[0].strip().lower() == "server-port":  # Server port needs to be an integer.
                settings_dictionary[key_value_setting[0].strip().lower()] = int(key_value_setting[-1].strip())
            else:
                # Everything else can be a string.
                settings_dictionary[key_value_setting[0].strip().lower()] = str(key_value_setting[-1].strip())

        return settings_dictionary


    def __get_config_file(self):
        """
        Gets the config template from github.
        :return:
        """

        config_template_url = "https://github.com/MrKelpy/MCSMs/blob/master/resources/CONFIG_TEMPLATE3.0.txt"
        self.__logger.log(f"Getting config template from {config_template_url}")
        data = requests.get(config_template_url)
        soup = BeautifulSoup(data.text, "html.parser")
        config_template = ""

        for line in soup.find_all("tr"):
            config_template += f"{line.text.strip()}\n"

        return config_template


    def __ensure_config_existance(self):
        """
        Ensures the existance of a config.mcsm file.
        :return:
        """

        # Checks if the config.mcsm file exists. If not, check the template on GitHub
        # and create the file.
        if not os.path.isfile(self.config_path):
            config_template = self.__get_config_file()

            with open(self.config_path, "w") as config_file:
                self.__logger.log(f"Creating mcsm.config file at {self.config_path}")
                config_file.write(config_template)