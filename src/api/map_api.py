#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests

from config.settings import MAP_API_URL, NO_DATA, DEFAULT_COORDINATES
from src.errors import HereNetworkError, HereJsonError, HereBadRequestError
from src.api.parser import Parser

class MapApi:
    """
        MapApi class
        To manage the map API data recovery
    """

    def __init__(self):
        """ Constructor """
        self.parser = Parser()
        self.cleaned_question = ''
        self.cleaned_question_words_list = []

    def get_raw_map_data(self, cleaned_question):
        """
            We get the information about the place searched by the user from
            the API.
            :param: cleaned_question is a string (the user question) after
            cleaning
            :return: locations returned by the API
            :rtype: JSON
        """
        # We define the parameters of the request
        params = {
            "apiKey": os.environ.get('HERE_JS_API_KEY'),
            "lang": "fr",
            "q": cleaned_question
            }
        try:
            result = requests.get(MAP_API_URL, params = params)
        except:
            print("The connection to the Here.com API has failed.")
            raise HereNetworkError()
        else:
            # If the request succeeds, we return the "items" key (which contains
            # the information we are interested in) of the json returned by the API
            try:
                if result.status_code == 200:
                    json_data = {}
            except:
                print("Bad request during MapApi.get_raw_map_data.")
                raise HereBadRequestError()
            else:
                try:
                    if 'items' in result.json() and len(result.json()['items']) > 0:
                        json_data = result.json()['items']
                        
                        return json_data
                except:
                    print("JSON does not contain map_data.")
                    raise HereJsonError

    def get_filtered_map_data_list(self, raw_map_data, string_words_list):
        """
            The API responses are filtered to reduce the number of responses
            and keep only the most relevant ones.
            We choose the first answer among those remaining after filtering
            :param: raw_map_data is a JSON with the information about the place
            searched by the user from the API.
            :return: coordinates (latitude and longitude) of the place
            :rtype: tuple
        """
        # Creation of a dictionary containing data from JSON data
        map_data_dict_list = [item for item in raw_map_data]

        # We compare the keywords of the user's question with those of the
        # "label" key of each answer provided by the API.
        # We keep only those whose "label" key contains all the keywords of the
        # user question
        filtered_map_data_list = []
        for item in map_data_dict_list:
            if 'address' in item.keys() and 'label' in item['address'].keys():            
                label = item['address']['label']
                parsed_label = self.parser.get_cleaned_string(label)
                if len(set(string_words_list).intersection(set(parsed_label.split(' ')))) > 0:
                    filtered_map_data_list.append(item)

        if not filtered_map_data_list:
            return DEFAULT_COORDINATES

        # We return the coordinates of the first place in the list
        return (
            filtered_map_data_list[0]['position']['lat'],
            filtered_map_data_list[0]['position']['lng']
            )

    def get_cleaned_map_data(self, raw_string):
        """
            We retrieve the coordinates of the user's location
            :param: raw_string is a string (the raw user question)
            :return: coordinates (latitude and longitude) of the location
            :rtype: tuple
        """
        # We retrieve the parsed data from the user's question.
        cleaned_question = self.parser.get_cleaned_string(raw_string)
        
        if cleaned_question == NO_DATA:
            print("La question de l'utilisateur est vide (map).")
            return DEFAULT_COORDINATES

        # We store the parsed list of words, for later use
        cleaned_question_words_list = self.parser.cleaned_string_words_list
        # We get all API response
        raw_map_data = self.get_raw_map_data(cleaned_question)

        if raw_map_data is None:
            return DEFAULT_COORDINATES

        # We return the first response after filtering
        return self.get_filtered_map_data_list(raw_map_data, cleaned_question_words_list)
