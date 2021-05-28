#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import requests
import sys

from config.settings import NO_DATA, DEFAULT_COORDINATES, DEFAULT_WIKI_DATA
from tests.raw_data_for_tests import NO_WIKI_DATA, RAW_WIKI_DATA_PAGE_TITLE, RAW_WIKI_COORDINATES, RAW_WIKI_EXTRACT, RAW_WIKI_PAGE_TITLE_AND_COORDINATES
from src import Parser
from src import WikiApi
from src.errors import WikiNetworkError, WikiJsonError, WikiBadRequestError

parser = Parser()
wikiApi = WikiApi()

##########################################################
############### Test of wiki_page_title() ################
##########################################################

def test_should_get_wiki_page_title(monkeypatch):
    """
        Test of wiki_page_title(), case 1
        Nominal case
    """
    cleaned_question = "notre-dame paris"
    
    class MockRequestsGet:
        def __init__(self, url, params=None):
            pass
        def json(self):
            return { "query": {
                        "search": [
                            { 
                             "title": RAW_WIKI_DATA_PAGE_TITLE
                            }
                        ]
                    }
                }
        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, 'get', MockRequestsGet)
    assert wikiApi.get_wiki_page_title(cleaned_question) == RAW_WIKI_DATA_PAGE_TITLE

def test_should_get_wiki_page_title_but_connection_fail(monkeypatch):
    """
        Test of wiki_page_title(), case 2
        Unable to connect to the API
    """
    with pytest.raises(WikiNetworkError):
        cleaned_question = "notre-dame paris"
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                raise requests.HTTPError('Unable to connect to the API')
            def json(self):
                pass
            def raise_for_status(self):
                pass

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_page_title(cleaned_question)

def test_should_get_wiki_page_title_but_bad_request(monkeypatch):
    """
        Test of wiki_page_title(), case 3
        Status code != 2xx
    """
    with pytest.raises(WikiBadRequestError):
        cleaned_question = "notre-dame paris"
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                pass
            def raise_for_status(self):
                raise requests.HTTPError('Status code other than 2xx')

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_page_title(cleaned_question)

def test_should_get_wiki_page_title_but_key_error(monkeypatch):
    """
        Test of wiki_page_title(), case 4
        We call a key that does not exist in the JSON response
    """
    with pytest.raises(WikiJsonError):
        cleaned_question = "notre-dame paris"
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                return { }
            def raise_for_status(self):
                pass

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_page_title(cleaned_question)

##########################################################
############# Test of get_wiki_coordinates() #############
##########################################################

def test_should_get_wiki_coordinates(monkeypatch):
    """
        Test of get_wiki_coordinates(), case 1
        Nominal case
    """
    wiki_page_title = RAW_WIKI_DATA_PAGE_TITLE
    
    class MockRequestsGet:
        def __init__(self, url, params=None):
            self.status_code = 200
        def json(self):
            return { "query": {
                        "pages": {
                            "12345": {
                                "coordinates": [
                                    RAW_WIKI_COORDINATES
                                ]
                            }
                        }
                    }
                }
        def raise_for_status(self):
                pass

    monkeypatch.setattr(requests, 'get', MockRequestsGet)
    assert wikiApi.get_wiki_coordinates(wiki_page_title) == (48.853056, 2.349722)

def test_should_get_wiki_coordinates_but_connection_fail(monkeypatch):
    """
        Test of get_wiki_coordinates(), case 2
        Unable to connect to the API
    """
    with pytest.raises(WikiNetworkError):
        wiki_page_title = RAW_WIKI_DATA_PAGE_TITLE
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                raise requests.HTTPError('Unable to connect to the API')
            def json(self):
                pass
            def raise_for_status(self):
                pass

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_coordinates(wiki_page_title)

def test_should_get_wiki_coordinates_but_bad_request(monkeypatch):
    """
        Test of get_wiki_coordinates(), case 3
        Status code != 2xx
    """
    with pytest.raises(WikiBadRequestError):
        wiki_page_title = RAW_WIKI_DATA_PAGE_TITLE
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                pass
            def raise_for_status(self):
                raise requests.HTTPError('Status code other than 2xx')

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_coordinates(wiki_page_title)

def test_should_get_wiki_coordinates_but_key_error(monkeypatch):
    """
        Test of get_wiki_coordinates(), case 4
        We call a key that does not exist in the JSON response
    """
    with pytest.raises(WikiJsonError):
        wiki_page_title = RAW_WIKI_DATA_PAGE_TITLE
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                return { }
            def raise_for_status(self):
                pass

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_coordinates(wiki_page_title)

##########################################################
############### Test of get_wiki_extract() ###############
##########################################################

def test_should_get_wiki_extract(monkeypatch):
    """
        Test of get_wiki_extract(), case 1
        Nominal case
    """
    wiki_page_title = RAW_WIKI_DATA_PAGE_TITLE
    
    class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                return { "query": {
                            "pages": {
                                "12345": {
                                    "extract": RAW_WIKI_EXTRACT
                                }
                            }
                        }
                    }
            def raise_for_status(self):
                pass

    monkeypatch.setattr(requests, 'get', MockRequestsGet)
    assert wikiApi.get_wiki_extract(wiki_page_title) == RAW_WIKI_EXTRACT

def test_should_get_wiki_extract_but_connection_fail(monkeypatch):
    """
        Test of wiki_page_title(), case 2
        Unable to connect to the API
    """
    with pytest.raises(WikiNetworkError):
        wiki_page_title = RAW_WIKI_DATA_PAGE_TITLE
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                raise requests.HTTPError('Unable to connect to the API')
            def json(self):
                pass
            def raise_for_status(self):
                pass

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_extract(wiki_page_title)

def test_should_get_wiki_extract_but_bad_request(monkeypatch):
    """
        Test of wiki_page_title(), case 3
        Status code != 2xx
    """
    with pytest.raises(WikiBadRequestError):
        wiki_page_title = RAW_WIKI_DATA_PAGE_TITLE
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                pass
            def raise_for_status(self):
                raise requests.HTTPError('Status code other than 2xx')

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_extract(wiki_page_title)

def test_should_get_wiki_extract_but_key_error(monkeypatch):
    """
        Test of wiki_page_title(), case 4
        We call a key that does not exist in the JSON response
    """
    with pytest.raises(WikiJsonError):
        wiki_page_title = RAW_WIKI_DATA_PAGE_TITLE
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                return { }
            def raise_for_status(self):
                pass

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_extract(wiki_page_title)

##########################################################
###### Test of get_wiki_page_title_and_coordinates() #####
##########################################################

def test_should_get_wiki_page_title_and_coordinates(monkeypatch):
    """
        Test of get_wiki_page_title_and_coordinates(), case 1
        Nominal case
    """
    here_coordinates = (48.89746, 2.38344)
    
    class MockRequestsGet:
            def __init__(self, url, params=None):
                self.status_code = 200
            def json(self):
                return { "query": {
                            "geosearch": [
                                RAW_WIKI_PAGE_TITLE_AND_COORDINATES
                            ]
                        }
                    }
            def raise_for_status(self):
                pass

    monkeypatch.setattr(requests, 'get', MockRequestsGet)
    assert wikiApi.get_wiki_page_title_and_coordinates(here_coordinates) == {
        "page_title": "Quai de la Gironde",
        "coordinates": (48.8965, 2.383164)
        }

def test_should_get_wiki_page_title_and_coordinates_but_no_here_coordinates(monkeypatch):
    """
        Test of get_wiki_page_title_and_coordinates(), case 2
        No coordinates case
    """
    here_coordinates = NO_DATA
    assert wikiApi.get_wiki_page_title_and_coordinates(here_coordinates) == NO_DATA
    
def test_should_get_wiki_page_title_and_coordinates_but_connection_fail(monkeypatch):
    """
        Test of wiki_page_title(), case 3
        Unable to connect to the API
    """
    with pytest.raises(WikiNetworkError):
        here_coordinates = (48.89746, 2.38344)
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                raise requests.HTTPError('Unable to connect to the API')
            def json(self):
                pass
            def raise_for_status(self):
                pass

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_page_title_and_coordinates(here_coordinates)

def test_should_get_wiki_page_title_and_coordinates_but_bad_request(monkeypatch):
    """
        Test of wiki_page_title(), case 4
        Status code != 2xx
    """
    with pytest.raises(WikiBadRequestError):
        here_coordinates = (48.89746, 2.38344)
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                pass
            def raise_for_status(self):
                raise requests.HTTPError('Status code other than 2xx')

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_page_title_and_coordinates(here_coordinates)

def test_should_get_wiki_page_title_and_coordinates_but_key_error(monkeypatch):
    """
        Test of wiki_page_title(), case 5
        We call a key that does not exist in the JSON response
    """
    with pytest.raises(WikiJsonError):
        here_coordinates = (48.89746, 2.38344)
        
        class MockRequestsGet:
            def __init__(self, url, params=None):
                pass
            def json(self):
                return { }
            def raise_for_status(self):
                pass

        monkeypatch.setattr(requests, 'get', MockRequestsGet)
        wikiApi.get_wiki_page_title_and_coordinates(here_coordinates)

##########################################################
######### Test of get_first_complete_wiki_data() #########
##########################################################

def test_should_get_first_complete_wiki_data(monkeypatch):
    """
        Test of get_first_complete_wiki_data(), case 1
        Nominal case
    """
    question = "Que peux-tu me dire à propos de Notre-Dame de Paris ?"
    
    def mock_get_cleaned_string(question):
        return "notre-dame paris"
    
    def mock_get_wiki_page_title(cleaned_question):
        return RAW_WIKI_DATA_PAGE_TITLE
    
    def mock_get_wiki_extract(wiki_page_title):
        return RAW_WIKI_EXTRACT
    
    def mock_get_wiki_coordinates(wiki_page_title):
        return (48.853056, 2.349722)
    
    monkeypatch.setattr(parser, 'get_cleaned_string', mock_get_cleaned_string)
    monkeypatch.setattr(wikiApi, 'get_wiki_page_title', mock_get_wiki_page_title)
    monkeypatch.setattr(wikiApi, 'get_wiki_extract', mock_get_wiki_extract)
    monkeypatch.setattr(wikiApi, 'get_wiki_coordinates', mock_get_wiki_coordinates)
    assert wikiApi.get_first_complete_wiki_data(question) == {
            "wiki_page_title": RAW_WIKI_DATA_PAGE_TITLE,
            "wiki_extract": RAW_WIKI_EXTRACT,
            "wiki_coordinates": (48.853056, 2.349722)
        }
    
def test_should_get_first_complete_wiki_data_but_empty_question(monkeypatch):
    """
        Test of get_first_complete_wiki_data(), case 2
        No coordinates case
    """
    cleaned_question = NO_DATA
    assert wikiApi.get_first_complete_wiki_data(cleaned_question) == DEFAULT_WIKI_DATA

##########################################################
######### Test of get_second_complete_wiki_data() ########
##########################################################

def test_should_get_second_complete_wiki_data(monkeypatch):
    """
        Test of get_second_complete_wiki_data(), case 1
        Nominal case
    """
    here_coordinates = (48.89746, 2.38344)
    
    def mock_get_wiki_page_title_and_coordinates(here_coordinates):
        return {
            "page_title": "Quai de la Gironde",
            "coordinates": (48.8965, 2.383164)
            }
    
    def mock_get_wiki_extract(wiki_page_title):
        return RAW_WIKI_EXTRACT
    
    monkeypatch.setattr(wikiApi, 'get_wiki_page_title_and_coordinates', mock_get_wiki_page_title_and_coordinates)
    monkeypatch.setattr(wikiApi, 'get_wiki_extract', mock_get_wiki_extract)
    assert wikiApi.get_second_complete_wiki_data(here_coordinates) == {
            "wiki_page_title": "Quai de la Gironde",
            "wiki_extract": RAW_WIKI_EXTRACT,
            "wiki_coordinates": (48.8965, 2.383164)
        }

def test_should_get_second_complete_wiki_data_but_no_here_coordinates(monkeypatch):
    """
        Test of get_second_complete_wiki_data(), case 2
        No coordinates case
    """
    here_coordinates = NO_DATA
    assert wikiApi.get_second_complete_wiki_data(here_coordinates) == DEFAULT_WIKI_DATA
