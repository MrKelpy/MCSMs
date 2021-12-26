# -*- coding: utf-8 -*-
# Created at 25/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
import subprocess

# Third Party Imports
# Local Application Imports

p = subprocess.Popen(["java", "--version"],
                 stdout=subprocess.PIPE)
print(type(p))