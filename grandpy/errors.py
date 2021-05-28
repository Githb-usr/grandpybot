#!/usr/bin/env python
# -*- coding: utf-8 -*-

class HereBadRequestError(Exception):
    """
        To capture request errors when connecting to the Here.com API
    """

class HereJsonError(Exception):
    """
        To catch errors due to empty or incomplete JSON from the Here.com API
    """

class HereNetworkError(Exception):
    """
        To capture network errors from the Here.com API
    """

class WikiBadRequestError(Exception):
    """
        To capture request errors when connecting to the Wikipedia API
    """

class WikiJsonError(Exception):
    """
        To catch errors due to empty or incomplete JSON from the Wikipedia API
    """

class WikiNetworkError(Exception):
    """
        To capture network errors from Wikipedia API
    """
