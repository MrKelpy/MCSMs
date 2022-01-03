# -*- coding: latin-1 -*-
# Created at 27/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
import os
import subprocess
import shutil

# Third Party Imports
# Local Application Imports

class MCSMGenerator:
    """
    This class implements an automated way to create
    new MCSM releases.
    """

    def __init__(self, mcsm_type: str, version: str, mcver: str):
        self.__icon_path = r"./icon.ico"
        self.__license_path = r"./LICENSE"
        self.__mcsm_type = mcsm_type
        self.__mcsm_folder_path = fr"../{self.__mcsm_type.title()}"
        self.__releases_path = r"./releases"
        self.__version = version
        self.__mcver = mcver
        self.__readme_path = "./README.txt"


    def run(self):
        """
        Creates a new MCSM release using pyinstaller.
        :return:
        """

        # Ensures a clean build folder everytime this method is called
        build_path = os.path.join(self.__releases_path, f"build-{mcsm_type}.{self.__version}")

        if os.path.exists(build_path):
            shutil.rmtree(build_path, ignore_errors=True)
        os.makedirs(build_path)

        # Copies all the code from the MCSM Type folder into the build folder.
        for file in os.listdir(self.__mcsm_folder_path):
            if not file.endswith(".py"): continue
            print(f"Copying '{file}' into '{build_path}'...")
            filepath = os.path.join(self.__mcsm_folder_path, file)
            shutil.copy(filepath, build_path)

        # Copies the icon.ico file into the build folder
        shutil.copy(self.__icon_path, build_path)

        # Builds the binary
        subprocess.run(["pyinstaller", "--onefile", f"--icon=icon.ico", "main.py"],
                       cwd=build_path)

        # Renames the binary to MCSM.exe and takes it out of the dist folder.
        binary_path = os.path.join(build_path, "dist", "main.exe")
        os.rename(binary_path, os.path.join(build_path, "dist", "MCSM.exe"))

        binary_path = os.path.join(build_path, "dist", "MCSM.exe")
        shutil.move(binary_path, build_path)

        # Deletes all the items in the build folder that aren't the binary
        for item in os.listdir(build_path):
            itempath = os.path.join(build_path, item)
            if item.endswith(".exe"): continue
            if os.path.isfile(itempath): os.remove(itempath)
            if os.path.isdir(itempath): shutil.rmtree(itempath, ignore_errors=True)

        # Adds the LICENSE and README.txt files into the build folder
        shutil.copy(self.__license_path, build_path)
        shutil.copy(self.__readme_path, build_path)

        # Zips everything up and deletes the build folder.
        release_path = os.path.join(self.__releases_path, fr"MCSMv{self.__version}-{self.__mcsm_type}.{self.__mcver}")
        shutil.make_archive(release_path, "zip", build_path)
        shutil.rmtree(build_path)

        print(f"Finished building MCSM-{self.__mcsm_type}.{self.__version}")


if __name__ == "__main__":
    mcsm_type = input("MCSM TYPE: ").strip()
    mcsm_version = input("MCSM VERSION: ").strip()
    server_version = input("MINECRAFT VERSION: ")
    MCSMGenerator(mcsm_type, mcsm_version, server_version).run()


