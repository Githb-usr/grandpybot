#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from dotenv import dotenv_values
from config.settings import MAP_API_URL
from app.api.parser import Parser

class MapApi:
    """
        MapApi class
        To manage the map API data recovery
    """

    def __init__(self):
        """ Constructor """
        self.parser = Parser()
        self.cleaned_question = ''
        self.parsed_data_list = []

    def get_raw_map_data(self, raw_data):
        """
            We get the information about the place searched by the user from
            the API.
            :param: raw_data is a string (the user question)
            :return: locations returned by the API
            :rtype: JSON
        """
        config = dotenv_values(".env")
        # We retrieve the parsed data from the user's question.
        self.parser.get_cleaned_data(raw_data)
        self.cleaned_question = self.parser.cleaned_data

        # We define the parameters of the request
        params = {
            "apiKey": config["HERE_JS_API_KEY"],
            "lang": "fr",
            "q": self.cleaned_question
            }
        result = requests.get(MAP_API_URL, params = params)

        # If the request succeeds, we return the "items" key (which contains
        # the information we are interested in) of the json returned by the API
        if result.status_code == 200:
            json_data = result.json()

            return json_data['items']
        # If the request fails, we restart it after 1 second of waiting.
        else:
            print("La connexion à l'API de Here.com a échoué.")
            print("Nouvelle tentative.")
            time.sleep(1)
            self.get_map_data()

    def filter_data_list(self, raw_data):
        """
            The API responses are filtered to reduce the number of responses
            and keep only the most relevant ones
            :param: raw_data is a string (the user question)
            :return: locations returned by the API but filtered
            :rtype: dictionary list
        """
        # We get the raw data from the API in JSON
        json_data = self.get_raw_map_data(raw_data)
        self.parsed_data_list = self.parser.parsed_data_list

        # Creation of a dictionary containing data from JSON data
        data_dict_list = []
        for item in json_data:
            data_dict_list.append(item)

        # We compare the keywords of the user's question with those of the
        # "label" key of each answer provided by the API.
        # We keep only those whose "label" key contains all the keywords of the
        # user question
        filtered_data_list = []
        parsed_labels = []
        for item in data_dict_list:
            label = item['address']['label']
            parsed_label = self.parser.get_cleaned_data(label)
            parsed_labels.append(parsed_label)
            if set(self.parsed_data_list) <= set(parsed_label.split(' ')):
                filtered_data_list.append(item)

        return filtered_data_list

    def choose_answer(self, raw_data):
        """
            We choose an answer among those remaining after filtering
            :param: raw_data is a string (the user question)
            :return: coordinates (latitude and longitude) of the place
            :rtype: tuple
        """
        filtered_data_list = self.filter_data_list(raw_data)

        # If the list is empty, default coordinates are returned (a point in
        # the Baltic Sea, in Europe)
        if len(filtered_data_list) == 0:
            return (54.525961, 15.255119)
        # otherwise we return the coordinates of the first place in the list
        else:
            return (filtered_data_list[0]['position']['lat'], filtered_data_list[0]['position']['lng'])
