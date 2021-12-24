# -*- coding: utf-8 -*-
# Created at 23/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
import traceback
import os

# Third Party Imports
# Local Application Imports
from MCSMApp import MCSMApp

if __name__ == "__main__":

    try:
         MCSMApp().run()
    except BaseException as err:
        # Resorts to directly writing a crude fatal traceback log into the
        # latest.log file.

        logs_folder = r".\server_files\mcsm_logs"
        os.makedirs(logs_folder, exist_ok=True)

        with open(fr".\{logs_folder}\latest.log", "a") as logsfile:
            logsfile.write(f"[FATAL ERROR] {traceback.format_exc()}\n")
