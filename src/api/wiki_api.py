#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dotenv import dotenv_values
import requests

from src.errors import WikiNetworkError, WikiJsonError, WikiBadRequestError
from src.api.parser import Parser
from config.settings import WIKI_API_URL, NO_DATA, DEFAULT_WIKI_DATA

class WikiApi:
    """
        WikiApi class
        To manage the Wikipedia API data recovery after use Here API
    """

    def __init__(self):
        """ Constructor """
        self.parser = Parser()

    def get_wiki_page_title(self, cleaned_question):
        """
            We get the title of the Wikipedia page from the API
            :return: the wiki page title (not parsed string)
            :rtype: string
        """
        if cleaned_question == NO_DATA:
            return NO_DATA

        # We define the parameters of the request
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": cleaned_question
        }
        try:
            result = requests.get(WIKI_API_URL, params = params)
        except:
            print("The connection to the Wikipedia API (for page title) has failed.")
            raise WikiNetworkError()
        else:
            try:
                if result.status_code == 200:
                    data = result.json()
            except:
                print("Bad request during WikipediaWikiMapApi.get_wiki_page_title().")
                raise WikiBadRequestError()
            else:
                try:
                    if 'query' in data.keys():
                        return data["query"]["search"][0]["title"]
                except:
                    print("The JSON does not contain the page title.")
                    raise WikiJsonError()

    def get_wiki_coordinates(self, wiki_page_title):
        """
            We get the place's wiki coordinates from the API
            :return: coordinates (latitude and longitude) of the location
            :rtype: tuple
        """
        if wiki_page_title == NO_DATA:
            return NO_DATA

        # We define the parameters of the request
        params = {
            "action": "query",
            "format": "json",
            "prop": "coordinates",
            "redirects": "",
            "titles": wiki_page_title
        }
        try:
            result = requests.get(WIKI_API_URL, params = params)
        except:
            print("The connection to the Wikipedia API (for coordinates) has failed.")
            raise WikiNetworkError()
        else:
            try:
                if result.status_code == 200:
                    data = result.json()
            except:
                print("Bad request during WikipediaWikiMapApi.get_wiki_coordinates().")
                raise WikiBadRequestError()
            else:
                try:
                    if 'query' in data.keys() and list(data["query"]["pages"].values())[0]["coordinates"][0]["lat"]:
                        return (
                            list(data["query"]["pages"].values())[0]["coordinates"][0]["lat"],
                            list(data["query"]["pages"].values())[0]["coordinates"][0]["lon"]
                            )
                except:
                    print("JSON does not contain coordinates.")
                    raise WikiJsonError()

    def get_wiki_extract(self, wiki_page_title):
        """
            We get the extract of wikipedia page for GrandPy's anecdote
            :param: wiki_page_title is a string
            :return: the extract (the beginning of the wikipedia page)
            :rtype: string
        """
        if wiki_page_title == NO_DATA:
            return NO_DATA

        # We define the parameters of the request
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exchars": 1200,
            "exintro": 1,
            "explaintext": 1,
            "titles": wiki_page_title
        }
        try:
            result = requests.get(WIKI_API_URL, params = params)
        except:
            print("The connection to the Wikipedia API (for extract) has failed.")
            raise WikiNetworkError()
        else:
            try:
                if result.status_code == 200:
                    data = result.json()
            except:
                print("Bad request during WikipediaWikiMapApi.get_wiki_extract().")
                raise WikiBadRequestError()
            else:
                try:
                    if 'query' in data.keys() and list(data['query']['pages'].values())[0]['extract']:
                        return list(data['query']['pages'].values())[0]['extract']
                except:
                    print("JSON does not contain an extract.")
                    raise WikiJsonError()

    def get_wiki_page_title_and_coordinates(self, coordinates):
        """
            We get the title of the Wikipedia page and
            the place's wiki coordinates from the wiki API
            :param: coordinates is a tuple with latitude and longitude of the
            place from map API.
            :return: the page title and place coordinates from Wikipedia
            :rtype: dictionary
        """
        if coordinates == NO_DATA:
            return NO_DATA

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
        try:
            result = requests.get(WIKI_API_URL, params = params)
        except:
            print("The connection to the Wikipedia API (for page title & coordinates) has failed.")
            raise WikiNetworkError()
        else:
            # If the request succeeds, we we retrieve only the data we are
            # interested in among all those present in the JSON obtained
            try:
                if result.status_code == 200:
                    raw_data = result.json()
            except:
                print("Bad request during get_page_title.")
                raise WikiBadRequestError()
            else:
                try:
                    if 'query' in raw_data.keys() and raw_data['query']['geosearch']:
                        data = raw_data['query']['geosearch'][0]
                    return {
                            "page_title": data['title'],
                            "coordinates": (data['lat'], data['lon'])
                            }
                except:
                    print("JSON does not contain page title & coordinates.")
                    raise WikiJsonError()

    def get_first_complete_wiki_data(self, raw_string):
        """
            We get all the wiki data.
            :param: raw_string is a string (the raw user question).
            :return: - title of the Wikipedia page
                     - extract of the Wikipedia page
                     - the place's wiki coordinates
            :rtype: dictionary
        """
        complete_wiki_data = {}
        cleaned_question = self.parser.get_cleaned_string(raw_string)
        
        if cleaned_question == NO_DATA:
            print("La question de l'utilisateur est vide (wiki).")
            return DEFAULT_WIKI_DATA

        # We get the title of the wiki page.
        wiki_page_title = self.get_wiki_page_title(cleaned_question)

        return {
            "wiki_page_title": wiki_page_title,
            "wiki_extract": self.get_wiki_extract(wiki_page_title),
            "wiki_coordinates": self.get_wiki_coordinates(wiki_page_title)
        }

    def get_second_complete_wiki_data(self, coordinates):
        """
            We recover an extract of Wikipedia page about the cleaned string
            from the API.
            :param: coordinates is a tuple with latitude and longitude of the
            place from map API.
            :return: - title of the Wikipedia page
                     - extract of the Wikipedia page
                     - the place's wiki coordinates
            :rtype: dictionary
        """
        if coordinates == NO_DATA:
            print("Il n'y a pas de coordonnées valides en provenance de Here.com")
            return DEFAULT_WIKI_DATA

        wiki_page_title_and_coordinates = self.get_wiki_page_title_and_coordinates(coordinates)

        return {
            "wiki_page_title": wiki_page_title_and_coordinates["page_title"],
            "wiki_extract": self.get_wiki_extract(wiki_page_title_and_coordinates["page_title"]),
            "wiki_coordinates": wiki_page_title_and_coordinates["coordinates"]
        }
