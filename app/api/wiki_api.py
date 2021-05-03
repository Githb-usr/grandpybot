#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
import requests
import time
from dotenv import dotenv_values
from config.settings import WIKI_URL
from app.api.map_api import MapApi
from app.api.parser import Parser

class WikiApi:
    """
        WikiApi class
        To manage the Wikipedia API data recovery
    """
    def __init__(self):
        """ Constructor """
        self.parser = Parser()

    def get_page_title(self, coordinates):
        """
            We get xxx
            :return: xxx
            :rtype: xxx
        """
        if coordinates != None:
            params = {
                "action": "query",
                "list": "geosearch",
                "format": "json",
                "gscoord": str(coordinates[0])+"|"+str(coordinates[1]),
                "gsradius": 250,
                "gslimit": 1,
                "utf8":''
            }
            result = requests.get(WIKI_URL, params = params)

            if result.status_code == 200:
                raw_data = result.json()
                try:
                    data = raw_data['query']['geosearch'][0]
                    parsed_data_title = self.parser.get_parsed_data(data['title'])

                    return (data['title'], (data['lat'], data['lon']))
                except ValueError:
                    return 'savapa'
            else:
                print("La connexion à l'API de Wikipédia a échoué.")
                print("Nouvelle tentative.")
                time.sleep(1)
                self.get_wikipedia_data()
        else:
            print('pas de coordonnées')

    def get_wikipedia_data(self, coordinates):
        """
            We recover an extract of Wikipedia page about the cleaned string.
            :return: dictionnary data
            :rtype: dict()
        """
        page_title = self.get_page_title(coordinates)

        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exchars": 1200,
            "exintro": 1,
            "explaintext": 1,
            "titles": page_title[0]
        }
        result = requests.get(WIKI_URL, params = params)

        if result.status_code == 200:
            data = result.json()
            wiki_title = list(data['query']['pages'].values())[0]['title']
            wiki_extract = list(data['query']['pages'].values())[0]['extract']
            wiki_coord = (page_title[1][0], page_title[1][1])

            return (wiki_title, wiki_extract, wiki_coord)
        else:
            print("La connexion à l'API de Wikipédia a échoué.")
            print("Nouvelle tentative.")
            self.get_wikipedia_data()
