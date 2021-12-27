# -*- coding: utf-8 -*-
# Created at 26/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
from datetime import datetime
import os
import zipfile
import threading

# Third Party Imports
# Local Application Imports


class MCSMLogger:
    """
    This class implements a custom logging system for usage in
    the MCSMs.
    """

    def __init__(self):
        now = datetime.now()
        self.__server_files_path = os.path.join(os.getcwd(), "server_files")
        self.__logs_folder = os.path.join(self.__server_files_path, "mcsm_logs")
        self._logging_session = f"{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}"
        self._latest_log = os.path.join(self.__logs_folder, "latest.log")
        self.__lock = threading.Lock()
        self._initialize_logging()


    def log(self, message: str, level: str="INFO", console=True):
        """
        Logs a given message into both the log file and the console.
        :return:
        """
        now = datetime.now()

        # This little piece of code adds a leading 0 before the minute if it is less than 2 characters long.
        lead = ""
        if now.minute < 10: lead = 0

        log_string = f"[{now.day}/{now.month}/{now.year} {now.hour}:{lead}{now.minute}][MCSM/{level}] {message.strip()}"

        with self.__lock:
            with open(self._latest_log, "a") as logfile:
                logfile.write(log_string + '\n')
            if console: print(log_string)


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
            zipped_log = os.path.join(self.__logs_folder, session + ".zip")
            zipfile.ZipFile(zipped_log, mode='w').write(self._latest_log)
            os.remove(self._latest_log)

        with open(self._latest_log, "w") as logfile:
            logfile.write(f"LOGGING SESSION #{self._logging_session}\n")
