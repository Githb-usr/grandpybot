#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
        self.parsed_data_string = ''
        self.parsed_data_list = []

    def get_raw_map_data(self, raw_data):
        """
            Retrieve information about the place you are looking for
            :return: json data
            :rtype: xxx
        """
        config = dotenv_values(".env")
        self.parser.get_parsed_data(raw_data)
        self.parsed_data_string = self.parser.parsed_data_string
        
        params = {
            "apiKey": config["HERE_JS_API_KEY"],
            "lang": "fr",
            "q": self.parsed_data_string
            }
        result = requests.get(MAP_API_URL, params = params)

        if result.status_code == 200:
            json_data = result.json()
            
            return json_data['items']
        else:
            print("La connexion à l'API de Here.com a échoué.")
            print("Nouvelle tentative.")
            time.sleep(1)
            self.get_map_data()
            
    def filter_data_list(self, raw_data):
        json_data = self.get_raw_map_data(raw_data)
        self.parsed_data_list = self.parser.parsed_data_list
        
        data_dict_list = []
        # Creation of a dictionary containing data
        for item in json_data:
            data_dict_list.append(item)
        
        filtered_data_list = []
        parsed_labels = []
        for item in data_dict_list:
            label = item['address']['label']
            parsed_label = self.parser.get_parsed_data(label)
            parsed_labels.append(parsed_label)
            if set(self.parsed_data_list) <= set(parsed_label.split(' ')):
                filtered_data_list.append(item)

        return filtered_data_list

    def choose_answer(self, raw_data):
        filtered_data_list = self.filter_data_list(raw_data)

        if len(filtered_data_list) == 0:  
            (54.525961, 15.255119)
        else:
            return (filtered_data_list[0]['position']['lat'], filtered_data_list[0]['position']['lng'])
