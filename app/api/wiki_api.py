#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from dotenv import dotenv_values
from config.settings import WIKI_API_URL
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
            We get the title of the Wikipedia page
            :param: coordinates is a tuple with latitude and longitude of the
            place from map API.
            :return: the page title and place coordinates from Wikipedia
            :rtype: dictionary
        """
        # We define the parameters of the request
        params = {
            "action": "query",
            "list": "geosearch",
            "format": "json",
            "gscoord": str(coordinates[0])+"|"+str(coordinates[1]),
            "gsradius": 250,
            "gslimit": 1,
            "utf8":''
        }
        result = requests.get(WIKI_API_URL, params = params)

        # If the request succeeds, we we retrieve only the data we are
        # interested in among all those present in the JSON obtained
        if result.status_code == 200:
            raw_data = result.json()
            try:
                data = raw_data['query']['geosearch'][0]

                return {"page_title": data['title'], "latitude": data['lat'],
                        "longitude": data['lon']}
            except ValueError:
                return 'savapa'
        # If the request fails, we restart it after 1 second of waiting.
        else:
            print("La connexion à l'API de Wikipédia a échoué.")
            print("Nouvelle tentative.")
            time.sleep(1)
            self.get_wikipedia_data()

    def get_wikipedia_data(self, coordinates):
        """
            We recover an extract of Wikipedia page about the cleaned string
            from the API.
            :param: coordinates is a tuple with latitude and longitude of the
            place from map API.
            :return: the page title, the page extract and the wikipedia
            coordinates of the place, often more accurate than the map API.
            :rtype: dictionary
        """
        # We get the title of the Wikipedia page to build the query.
        wiki_title_coord = self.get_page_title(coordinates)
        page_title = wiki_title_coord["page_title"]

        # We define the parameters of the request
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exchars": 1200,
            "exintro": 1,
            "explaintext": 1,
            "titles": page_title
        }
        result = requests.get(WIKI_API_URL, params = params)

        # If the request succeeds, we build a dictionary containing the
        # following 3 pieces of information: title of the page, excerpt of
        # the page and coordinates proposed by Wikipedia
        if result.status_code == 200:
            data = result.json()
            wiki_title = list(data['query']['pages'].values())[0]['title']
            wiki_extract = list(data['query']['pages'].values())[0]['extract']
            wiki_coord = (wiki_title_coord["latitude"],
                          wiki_title_coord["longitude"])

            return {"wiki_title": wiki_title, "wiki_extract": wiki_extract,
                    "wiki_coord": wiki_coord}
        # If the request fails, we restart it after 1 second of waiting.
        else:
            print("La connexion à l'API de Wikipédia a échoué.")
            print("Nouvelle tentative.")
            time.sleep(1)
            self.get_wikipedia_data()
