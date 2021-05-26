#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import requests
import sys

from config.settings import DEFAULT_COORDINATES
from tests.raw_data_for_tests import NO_MAP_DATA, RAW_MAP_DATA_OK, NON_RELEVANT_MAP_DATA
from src import MapApi
from src import Parser
from src.errors import HereNetworkError, HereJsonError, HereBadRequestError

mapApi = MapApi()
parser = Parser()

def test_should_get_raw_map_data(monkeypatch):
    """
        Test of get_raw_map_data(), case 1
        Nominal case
    """
    cleaned_question = "musee confluences lyon"
    
    class MockRequestsGet:
        def __init__(self, url, params=None):
            self.status_code = 200
        def json(self):
            return { 'items': RAW_MAP_DATA_OK }

    monkeypatch.setattr(requests, 'get', MockRequestsGet)
    assert mapApi.get_raw_map_data(cleaned_question) == RAW_MAP_DATA_OK

# def test_should_get_raw_map_data_but_request_fail(monkeypatch):
#     """
#         Test of get_raw_map_data(), case 2
#         Status code != 200
#     """
#     with pytest.raises(HereBadRequestError):
#         cleaned_question = "musee confluences lyon"
        
#         class MockRequestsGet:
#             def __init__(self, url, params=None):
#                 self.status_code = 503
#             def json(self):
#                 return { 'items': RAW_MAP_DATA_OK }

#         monkeypatch.setattr(requests, 'get', MockRequestsGet)
#         mapApi.get_raw_map_data(cleaned_question)

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
 
def test_should_get_cleaned_map_data(monkeypatch):
    """
        Test of get_cleaned_map_data(), case 1
        Nominal case
    """
    question = "Bonjour, que peux-tu me dire à propos du musée des Confluences à Lyon ?"
    
    def mock_get_cleaned_string(string):
        return "musee confluences lyon"
    
    def mock_get_raw_map_data(string):
        return RAW_MAP_DATA_OK
    
    monkeypatch.setattr(parser, 'get_cleaned_string', mock_get_cleaned_string)
    monkeypatch.setattr(mapApi, 'get_raw_map_data', mock_get_raw_map_data)
    parser.cleaned_string_words_list = ['musee', 'confluences', 'lyon']
    cleaned_map_data = mapApi.get_cleaned_map_data(question)
    assert cleaned_map_data == (45.73374, 4.81744)

def test_should_get_default_coordinates_but_empty_or_spaces_string(monkeypatch):
    """
        Test of get_cleaned_map_data(), case 2
        Spaces or empty user question case
    """
    question = ""

    def mock_get_cleaned_string(string):
        return ""

    monkeypatch.setattr(parser, 'get_cleaned_string', mock_get_cleaned_string)
    cleaned_map_data = mapApi.get_cleaned_map_data(question)
    assert cleaned_map_data == DEFAULT_COORDINATES

def test_should_get_cleaned_map_data_but_no_data(monkeypatch):
    """
        Test of get_cleaned_map_data(), case 3
        No data case
    """
    question = "shgfhsdghjsdg"

    def mock_get_cleaned_string(string):
        return "shgfhsdghjsdg"

    def mock_get_raw_map_data(string):
        return NO_MAP_DATA

    monkeypatch.setattr(parser, 'get_cleaned_string', mock_get_cleaned_string)
    monkeypatch.setattr(mapApi, 'get_raw_map_data', mock_get_raw_map_data)
    parser.cleaned_string_words_list = ['shgfhsdghjsdg']
    cleaned_map_data = mapApi.get_cleaned_map_data(question)
    assert cleaned_map_data == DEFAULT_COORDINATES
