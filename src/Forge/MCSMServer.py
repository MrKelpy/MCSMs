# -*- coding: utf-8 -*-
# Created at 20/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
import contextlib
import os
import shutil
import sys
import subprocess
import socket

# Third Party Imports
import requests
from bs4 import BeautifulSoup

# Local Application Imports
from MCSMLogger import MCSMLogger
from MCSMConfig import MCSMConfig


class MCSMServer(MCSMConfig):
    """
    This class implements the main operations of the program,
    such as starting the server, managing downloads, etc...
    This class inherits from MCSMConfig to access the settings.
    """

    def __init__(self, logger: MCSMLogger):
        super().__init__(logger)

        # Essential properties to define the server "identity"
        self.version = "1.16.5"
        self.resources_url = "https://dl.dropbox.com/s/7emia0zggpyxld8/RESOURCES.zip?dl=0"

        # Properties to be used during execution
        self._server_files_path = os.path.join(os.getcwd(), "server_files")
        self._server_path = os.path.join(self._server_files_path, f"forge-{self.version}.jar")
        self.__logger = logger
        self.__ensure_file_integrity()
        self._settings = self.load_settings()

        if not self._settings["server-ip"]:
            self._settings["server-ip"] = socket.gethostbyname(socket.gethostname())

        self.__verify_port()


    def start(self):
        """
        This function will manage the entire server behaviour, by starting
        all the threads, and running all the functions or methods in the program.
        :return:
        """

        # Checks if the eula.txt file doesn't exist.
        # If it doesn't exist, run the server once ignoring the output
        # and then agree to the eula.
        if not self.__agree_to_eula():

            self.add_separator()
            # Performs an initialization run to create the eula
            self.__logger.log("Initializing Server... (Phase 1)")
            proc = self.__start_server()
            self.__process_output(proc, output=False)
            self.__agree_to_eula()
            self.__logger.log("Agreed to Mojang's EULA.")

            # Performs an initialization run to create the properties
            self.__logger.log("Initializing Server... (Phase 2)")
            proc = self.__start_server()
            self.__process_output(proc, output=True, exit_at="Loading properties")


        # Print the server information, and start it.
        self.__logger.log("Starting Server...", level="SERVER")
        self.add_separator()
        print(f"""
Minecraft Server Makers - {__copyright__}
Running {self._settings["server_name"]}
IP Address: {self._settings["server-ip"]}:{self._settings["server-port"]}
Version: Forge {self.version}
Allocated RAM: {self._settings["allocated_ram"]}MB ({int(self._settings["allocated_ram"])/1024} GB)
> REQUIRES LAN CONNECTION <
Recommended: https://www.radmin-vpn.com/
        """.strip())
        self.add_separator()
        self.__load_configs()  # Load the configurations from the config.mcsm file into the server.properties file.

        # Warns the user that running a server with less than 3GB might cause issues.
        if int(self._settings["allocated_ram"]) < 3072:
            self.__logger.log(f"The allocated ram is set to {self._settings['allocated_ram']}MB. "
                              f"Running a server with less than 3GB of memory might cause performance "
                              f"issues.", level="WARN")

        proc = self.__start_server()
        self.__process_output(proc)


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


    def __ensure_file_integrity(self):
        """
        Ensures that the server is capable of being run by detecting if
        all the files exist in the directory.
        :return:
        """
        self.add_separator()
        self.__logger.log("Ensuring file integrity...")

        # Create the server files folder if it doesn't already exist
        if not os.path.isdir(self._server_files_path):
            os.makedirs(self._server_files_path, exist_ok=True)
            self.__logger.log(f"Created server_files folder at {self._server_files_path}")

        # Checks if the config.mcsm file exists. If not, check the template on GitHub
        # and create the file.
        if not os.path.isfile(self.config_path):
            config_template = self.__get_config_file()

            with open(self.config_path, "w") as config_file:
                self.__logger.log(f"Creating mcsm.config file at {self.config_path}")
                config_file.write(config_template)

        # Checks if the forge jar is present inside the server files folder.
        for item in os.listdir(self._server_files_path):
            if f"minecraft_server.{self.version}" in item:
                break
        else:
            self.__logger.log("Minecraft Server JAR file not detected. Ensuing downloads...")
            self.__download_resources()
            pass


    def __download_resources(self):
        """
        Downloads all the necessary resources from the url to run the bot.
        These resources are composed of libraries, the forge and server.
        :return:
        """
        self.add_separator()
        resources_downloading_path = os.path.join(self._server_files_path, "downloading.zip")
        resources_downloaded_path = os.path.join(self._server_files_path, f"RESOURCES.zip")

        # Removes any files blocking up the paths
        with contextlib.suppress(FileNotFoundError):
            os.remove(resources_downloaded_path)
            os.remove(resources_downloading_path)

        self.__logger.log("DOWNLOADING RESOURCE FILES...")
        self.__logger.log(f"URL: {self.resources_url}")
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
        os.rename(resources_downloading_path, resources_downloaded_path)
        shutil.unpack_archive(resources_downloaded_path, extract_dir=self._server_files_path)
        os.remove(resources_downloaded_path)


    def __verify_port(self):
        """
        Verifies if the set port is available and ready to be used.
        If not, jumps to the next one, and repeats that until it finds
        a usable port.
        :return:
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            while True:
                self.__logger.log(f'Testing PORT "{self._settings["server-port"]}" with HOST "{self._settings["server-ip"]}"', console=False)

                # Tests a connection to a given server:port.
                # If it works and returns a code 0, it's being used.
                try:
                    sock.bind((self._settings["server-ip"], self._settings["server-port"]))
                    self.__logger.log(f'PORT "{self._settings["server-port"]}" is open, Server IP is now set to {self._settings["server-ip"]}:{self._settings["server-port"]}', console=False)
                    break
                except socket.error:

                    # Skips to the next port if the current port is being used
                    self.__logger.log(f'PORT "{self._settings["server-port"]}" is being used, trying PORT {self._settings["server-port"] + 1}', console=False)
                    self._settings["server-port"] += 1


    def __agree_to_eula(self):
        """
        Agrees to Mojang's EULA.
        :return: Boolean, True if the eula was agreed to, False if the eula.txt file didn't exist.
        """
        # Return False if the eula file does not exist.
        eula_path = os.path.join(self._server_files_path, "eula.txt")
        if not os.path.isfile(eula_path):
            return False

        # Opens the eula to save their lines into memory,
        # Checks if eula is already agreed to. If so, return True.
        with open(eula_path, "r") as eula:
            lines = eula.readlines()
            if lines[-1] == "eula=true": return True
            lines.pop(-1)

        # Writes all the normal lines into the eula, but at last
        # writes the eula=true line, indicative of agreement.
        with open(eula_path, "w") as eula:
            for line in lines:
                eula.write(line)
            eula.write("eula=true")
        return True


    def __start_server(self):
        """
        Runs the subprocess command to start the server,
        and returns the process for usage later on.
        :return: Subprocess.Popen
        """

        proc = subprocess.Popen(
            ["java", f'-Xmx{self._settings["allocated_ram"]}M', f'-Xms{self._settings["allocated_ram"]}M', '-jar', f'{self._server_path}', 'nogui'],
            cwd=self._server_files_path,
            stdout=subprocess.PIPE,
        )
        return proc


    def __process_output(self, proc: subprocess.Popen, exit_at: str = None, output: bool = True):
        """
        Handles any operation to be done with the output from
        the server.
        :param output: If set to True, won't log any output
        :param exit_at: String to exit the run when reached.
        :return:
        """

        last_out = str()
        for line in proc.stdout:

            # Prevent the same line from being logged more than once
            if line == last_out:
                continue

            # Log the decoded message from the minecraft log
            decoded_log = line.decode("UTF-8").strip()

            # Exits the process if a line was reached
            if exit_at and exit_at in decoded_log:
                proc.terminate()
                break

            last_out = line
            parsed_decoded_log, level = self._parse_mc_logs(decoded_log)
            self.__logger.log(parsed_decoded_log, level=f"SERVER/{level}", console=output)

            # Checks if the subproccess has been terminated, if so, break.
            if proc.poll() is not None:
                break


    def __load_configs(self):
        """
        Loads the configurations from the settings file
        into the server.properties file. (At least the ones that apply.)
        :return:
        """
        mcsm_setting_keys = self._settings.keys()
        properties_path = os.path.join(self._server_files_path, "server.properties")
        with open(properties_path, "r") as properties_file:
            properties = properties_file.readlines()

        # This list comprehension changes all server.properties with the same names as
        # any setting in the settings for their key=value equivalent in config.mcsm
        updated_properties = list()
        for line in properties:
            property_key = line.split('=')[0]

            if property_key in mcsm_setting_keys:
                updated_properties.append(f"{property_key}={self._settings[property_key]}\n")
            else:
                updated_properties.append(line)

        with open(properties_path, "w") as properties_file:
            properties_file.writelines(updated_properties)


    @staticmethod
    def add_separator():
        """
        Adds a separation line consisting of many "-" for visual enhancement.
        :return:
        """
        print("-"*125)


    @staticmethod
    def _parse_mc_logs(mclog: str):
        """
        Parses out the additional date and thread information from the mc logs,
        leaving only the message to be returned.
        :return: String, containing the mclog message; String, containing the logging level.
        """

        # All mc logs separate the additional info from the message with a ]:
        # So, split the log in its first occurence and return everything after it.
        info_separator = mclog.find("]:")

        # If the separator isn't found, return the raw mclog, since it's only a message.
        if info_separator == -1:
            return mclog, "INFO"

        message = mclog[info_separator+2:]
        level = [x for x in mclog[:info_separator].split("/") if x][-1]
        return message.strip(), level
