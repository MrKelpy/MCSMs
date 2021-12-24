# -*- coding: utf-8 -*-
# Created at 20/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
from datetime import datetime
import contextlib
import zipfile
import os
import sys

# Third Party Imports
import requests
from bs4 import BeautifulSoup

# Local Application Imports
from exceptions import ImpossibleDownload


class MCSMApp:
    """
    Class implementing the starting point for the program and the some essential
    operations for the server to start.
    """

    def __init__(self):

        # Properties to be used during execution
        now = datetime.now()
        self._server_files_path = os.path.join(os.getcwd(), "server_files")
        self._logging_session = f"{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}"
        self._logs_folder = os.path.join(self._server_files_path, "mcsm_logs")
        self._latest_log = os.path.join(self._logs_folder, "latest.log")
        self._initialize_logging()

        # Essential properties to define the server "identity"
        self.version = "1.18"
        self.resources_url = self._build_resources_url()
        self._ensure_file_integrity()


    def _initialize_logging(self):
        """
        Archives any dangling "latest.log" files, and creates a new latest.log file.
        :return:
        """
        os.makedirs(os.path.dirname(self._latest_log), exist_ok=True)

        if os.path.isfile(self._latest_log):

            # Acquire the session ID from the latest.log file.
            with open(self._latest_log, "r") as latestlog:
                session = latestlog.readlines()[0].split()[2][1:]

            # Make a .zip folder with the latest.log file
            zipped_log = os.path.join(self._logs_folder, session + ".zip")
            zipfile.ZipFile(zipped_log, mode='w').write(self._latest_log)
            os.remove(self._latest_log)

        with open(self._latest_log, "w") as logfile:
            logfile.write(f"LOGGING SESSION #{self._logging_session}\n")


    def _build_resources_url(self):
        """
        Takes into account the specified server version and obtains the
        direct download url from mcversions.net.
        This method is only meant to be used once during constructing.
        :return: String (url)
        """
        data = requests.get(f"https://mcversions.net/download/{self.version}")

        if data.status_code != 200:
            raise ImpossibleDownload(f"Code {data.status_code}, "
                                     f"download will never work @https://mcversions.net/download/{self.version}")

        soup = BeautifulSoup(data.text, "html.parser")
        url = [link["href"] for link in soup.find_all("a") if "server.jar" in link["href"]][0]
        return url



    def _get_config_file(self):
        """

        :return:
        """


    def _ensure_file_integrity(self):
        """
        Ensures that the server is capable of being run by detecting if
        all the files exist in the directory.
        :return:
        """
        self.log("Ensuring file integrity...")

        # Create the server files folder if it doesn't already exist
        if not os.path.isdir(self._server_files_path):
            os.makedirs(self._server_files_path, exist_ok=True)
            self.log(f"Created server_files folder at {self._server_files_path}")

        # Checks if the forge jar is present inside the server files folder.
        for item in os.listdir(self._server_files_path):
            if f"minecraft_server.{self.version}" in item:
                break
        else:
            self.log("Minecraft Server JAR file not detected. Ensuing downloads...")
            self._download_resources()
            pass


    def _download_resources(self):
        """
        Downloads all the necessary resources from the url to run the bot.
        These resources are composed of libraries, the forge and server.
        :return:
        """
        self.add_separator()
        resources_downloading_path = os.path.join(self._server_files_path, "downloading.jar")
        resources_downloaded_path = os.path.join(self._server_files_path, f"minecraft_server.{self.version}.jar")

        # Removes any files blocking up the paths
        with contextlib.suppress(FileNotFoundError):
            os.remove(resources_downloaded_path)
            os.remove(resources_downloading_path)

        self.log("DOWNLOADING RESOURCE FILES...")
        self.log(f"URL: {self.resources_url}")
        sys.stdout.write("\r" + f"PROGRESS:{' ' * 102}(0.0%)")
        sys.stdout.flush()

        with requests.get(self.resources_url, stream=True) as r:
            # Downloads the server resources needed for the mcsm to work.

            content_size = int(r.headers.get('content-length', 0)) / (1024 * 1024)
            with open(resources_downloading_path, "wb") as server_jar:

                total_downloaded = 0
                for chunk in r.iter_content(chunk_size=(1024 * 512)):
                    # Iterates through the data chunks, downloading a fair amount of bytes per turn
                    server_jar.write(chunk)

                    total_downloaded += len(chunk) / (1024 * 1024)
                    percentage = (100 * total_downloaded) / content_size + 0.1
                    progress_bar = f"PROGRESS: {'#' * int(percentage)} {' ' * int(100 - int(percentage))}({round(percentage - 0.1, 1)}%)"

                    sys.stdout.write("\r" + progress_bar)
                    sys.stdout.flush()

        print()
        self.add_separator()
        os.rename(resources_downloading_path, resources_downloaded_path, )


    @staticmethod
    def add_separator():
        """
        Adds a separation line consisting of many "-" for visual enhancement.
        :return:
        """
        print("-"*125)


    def log(self, message: str, level: str="INFO"):
        """
        Logs a given message into both the log file and the console.
        :return:
        """
        now = datetime.now()
        log_string = f"[{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}][MCSM/{level}] {message}\n"

        with open(self._latest_log, "a") as logfile:
            logfile.write(log_string)
        print(log_string)


    def agree_to_eula(self):
        """
        Changes the eula agreement to True, therefore agreeing
        to the EULA.
        :return:
        """


    def run(self):
        """
        This function will manage the entire server behaviour, by starting
        all the threads, and running all the functions or methods in the program.
        :return:
        """

