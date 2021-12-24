# -*- coding: utf-8 -*-
# Created at 22/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
# Third Party Imports
# Local Application Imports

tlist = ["a", "b", "d"]

for item in tlist:
    if "c" in item:
        break
else:
    print("hi")
