# -*- coding: utf-8 -*-
# Created at 26/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
from datetime import datetime
import os
import tarfile

# Third Party Imports
# Local Application Imports
import time

from Forge.MCSMLogger import MCSMLogger
from Forge.MCSMConfig import MCSMConfig


class MCSMBackups(MCSMConfig):
    """
    This class implements a periodical backups system which will be built-in the server.
    This class inherits from MCSMConfig to access the settings.
    """

    def __init__(self, logger: MCSMLogger):
        super().__init__(logger)

        self.__logger = logger
        self._server_files_path = os.path.join(os.getcwd(), "server_files")
        self._config_path = os.path.join(self._server_files_path, "config.mcsm")
        self._settings = self.load_settings()

        if not self._settings["backups-path"] or not os.path.exists(self._settings["backups-path"]):
            self.__backups_path = os.path.join(self._server_files_path, "MCSM-Backups", "Server")
            self.__logger.log(f"Backups path is unspecified or does not exist. "
                              f"Defaulted to {self.__backups_path}.", level="BACKUPS/WARN")
        else:
            self.__backups_path = self._settings["backups-path"]

        os.makedirs(self.__backups_path, exist_ok=True)


    def start(self):
        """
        Starts the backups system taking into account the
        defined settings for conditioning the system.
        :return:
        """

        # If the backups are set to False in the configs, don't do any backups.
        if self._settings["backups"] == "False":
            self.__logger.log("The backups setting is set to False, so no backups will be made. "
                              "You can change this by going to settings and "
                              "changing the \"BACKUPS\" setting to True.", level="BACKUPS/INFO")
            return

        while True:
            # Create a backup and wait for a configured amount of time.
            saved_path = self.__do_backup()

            # Check if the user wants to be notified about the backup.
            if self._settings["backups-notify"] == "True":
                self.__logger.log(f"Backup created. Saved at '{saved_path}'.",
                                  level="BACKUPS/INFO")

            time.sleep(float(self._settings["backups-cooldown"]))


    def __do_backup(self):
        """
        Zips the world folder and puts the .zip into
        the backups path. Ignores the session.lock file.
        :return:
        """
        world_folder = os.path.join(self._server_files_path, "world")
        now = datetime.now()
        backup_filename = f"{now.year}-{now.month}-{now.day}.{now.hour}.{now.minute}.tar.gz"
        output_path = os.path.join(self.__backups_path, backup_filename)

        # Prevents two backups with the same name
        if os.path.isfile(output_path):
            os.remove(output_path)

        # Makes the backup, filtering out the session.lock file.
        exclude = ["world/session.lock"]
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(world_folder, arcname="", filter=lambda x: None if x.name in exclude else x)

        return output_path
