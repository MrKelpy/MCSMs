# -*- coding: latin-1 -*-
# Created at 23/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
import threading
import traceback
import os

# Third Party Imports
# Local Application Imports
import exceptions
from MCSMServer import MCSMServer
from MCSMBackups import MCSMBackups
from MCSMPlayerdataBackups import MCSMPlayerdataBackups
from MCSMLogger import MCSMLogger

if __name__ == "__main__":

    try:
        print("-"*125)
        logger = MCSMLogger()
        backups_thread = threading.Thread(target=MCSMBackups(logger).start, daemon=True)
        playerdata_backups_thread = threading.Thread(target=MCSMPlayerdataBackups(logger).start, daemon=True)
        playerdata_backups_thread.start()
        backups_thread.start()
        MCSMServer(logger).start()

    except:
        # Resorts to directly writing a crude fatal traceback log into the
        # latest.log file.

        logs_folder = r".\server_files\mcsm_logs"
        os.makedirs(logs_folder, exist_ok=True)
        with open(fr".\{logs_folder}\latest.log", "a") as logsfile:
            logsfile.write(f"[FATAL ERROR] {traceback.format_exc()}\n")

        raise exceptions.FatalException(traceback.format_exc())
