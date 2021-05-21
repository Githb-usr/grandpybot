#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests

from src.errors import HereNetworkError, HereJsonError, HereBadRequestError
from src.api.parser import Parser
from config.settings import MAP_API_URL

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
        # config = dotenv_values(".env")

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
                    json_data = result.json()
            except:
                print("Bad request during MapApi.get_raw_map_data.")
                raise HereBadRequestError()
            else:
                try:
                    if 'items' in json_data.keys() and len(json_data['items']) != 0:
                        return json_data['items']
                except:
                    print("JSON does not contain map_data.")
                    raise HereJsonError()

    def get_filtered_map_data_list(self, raw_map_data):
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
        map_data_dict_list = []
        for item in raw_map_data:
            map_data_dict_list.append(item)

        # We compare the keywords of the user's question with those of the
        # "label" key of each answer provided by the API.
        # We keep only those whose "label" key contains all the keywords of the
        # user question
        filtered_map_data_list = []
        parsed_labels = []
        for item in map_data_dict_list:
            label = item['address']['label']
            parsed_label = self.parser.get_cleaned_string(label)
            parsed_labels.append(parsed_label)
            if set(self.cleaned_question_words_list) <= set(parsed_label.split(' ')):
                filtered_map_data_list.append(item)

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
        self.cleaned_question = self.parser.get_cleaned_string(raw_string)
        # We store the parsed list of words, for later use
        self.cleaned_question_words_list = self.parser.cleaned_string_words_list
        # We get all API response
        raw_map_data = self.get_raw_map_data(self.cleaned_question)

        # We return the first response after filtering
        return self.get_filtered_map_data_list(raw_map_data)