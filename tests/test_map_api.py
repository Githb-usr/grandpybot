#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from config.settings import MAP_API_URL, NO_DATA, DEFAULT_COORDINATES
from config.tests_settings import RAW_MAP_DATA_OK, NO_MAP_DATA, NON_RELEVANT_MAP_DATA
from src import MapApi
from src import Parser

mapApi = MapApi()
parser = Parser()

def test_should_get_raw_map_data(monkeypatch):
    """
        Test of get_raw_map_data()
    """
    cleaned_question = "musee confluences lyon"
    
    class MockRequestsGet:
        def __init__(self, url, params=None):
            self.status_code = 200
        def json(self):
            return { 'items': RAW_MAP_DATA_OK }

    monkeypatch.setattr(requests, 'get', MockRequestsGet)

    assert mapApi.get_raw_map_data(cleaned_question) == RAW_MAP_DATA_OK

def test_should_get_filtered_map_data_list(monkeypatch):
    """
        Test of get_filtered_map_data_list(), case 1
        Nominal case
    """
    question = "Bonjour, que peux-tu me dire à propos du musée des Confluences à Lyon ?"
    raw_map_data = RAW_MAP_DATA_OK
    cleaned_string_words_list = ['musee', 'confluences', 'lyon']
    
    def mock_get_cleaned_string(string):
        return "musee confluences 69002 lyon france"

    monkeypatch.setattr(parser, 'get_cleaned_string', mock_get_cleaned_string)

    final_coordinates = mapApi.get_filtered_map_data_list(raw_map_data, cleaned_string_words_list)

    assert final_coordinates == (45.73374, 4.81744)

def test_should_get_filtered_map_data_list_but_non_relevant_map_data(monkeypatch):
    """
        Test of get_filtered_map_data_list(), case 2
        Non relevant data
    """
    question = "Bonjour, que peux-tu me dire à propos de Notre-Dame de paris ?"
    raw_map_data = NON_RELEVANT_MAP_DATA
    cleaned_string_words_list = ['notre-dame', 'paris']
    
    def mock_get_cleaned_string(string):
        return "rue champs lyon france"
    
    monkeypatch.setattr(parser, 'get_cleaned_string', mock_get_cleaned_string)
    
    final_coordinates = mapApi.get_filtered_map_data_list(raw_map_data, cleaned_string_words_list)
    
    assert final_coordinates == DEFAULT_COORDINATES
    
def test_should_get_filtered_map_data_list_but_no_map_data(monkeypatch):
    """
        Test of get_filtered_map_data_list(), case 3
        No usable data
    """
    question = "shgfhsdghjsdg"
    raw_map_data = NO_MAP_DATA
    cleaned_string_words_list = ['shgfhsdghjsdg']
    
    def mock_get_cleaned_string(string):
        return "shgfhsdghjsdg"
    
    monkeypatch.setattr(parser, 'get_cleaned_string', mock_get_cleaned_string)
    
    final_coordinates = mapApi.get_filtered_map_data_list(raw_map_data, cleaned_string_words_list)
    
    assert final_coordinates == DEFAULT_COORDINATES
 
def test_should_get_cleaned_map_data():
    """
        Test of get_cleaned_map_data(), case 1
        Nominal case
    """
    question = "Bonjour, que peux-tu me dire à propos du musée des Confluences à Lyon ?"
    # cleaned_map_data = mapApi.get_cleaned_map_data(question)
    
    # assert cleaned_map_data == (45.73374, 4.81744)

def test_should_get_default_coordinates_but_spaces_string():
    """
        Test of get_cleaned_map_data(), case 2
        Spaces user question case
    """
    question = "   "
    cleaned_map_data = mapApi.get_cleaned_map_data(question)
    
    assert cleaned_map_data == DEFAULT_COORDINATES
    
def test_should_get_default_coordinates_but_empty_string():
    """
        Test of get_cleaned_map_data(), case 2
        Empty user question case
    """
    question = ""
    cleaned_map_data = mapApi.get_cleaned_map_data(question)
    
    assert cleaned_map_data == DEFAULT_COORDINATES

def test_should_get_cleaned_map_data_but_no_data():
    """
        Test of get_cleaned_map_data(), case 3
        No data case
    """
    question = "shgfhsdghjsdg"
    # cleaned_map_data = mapApi.get_cleaned_map_data(question)
    
    # assert cleaned_map_data == DEFAULT_COORDINATES
