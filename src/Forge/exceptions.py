# -*- coding: utf-8 -*-
# Created at 23/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
# Third Party Imports
# Local Application Imports

class ImpossibleDownload(BaseException):
    """
    This exception is invoked whenever a download is
    unsuccessful or will never be successful.
    """


class FatalException(BaseException):
    """
    This exception is invoked whenenver a fatal error happens.
    """