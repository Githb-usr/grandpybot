#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.settings import STOPWORDS, NO_DATA
from src import Parser

parser = Parser()

def test_should_refuse_empty_string():
    """
        Test of refuse_empty_string(), Case 1
        The string is empty
    """
    question = ""
    refusal = parser.refuse_empty_string(question)
    
    assert refusal == NO_DATA
    
def test_should_refuse_spaces_string():
    """
        Test of refuse_empty_string(), Case 2
        The string consists of spaces
    """
    question = "         "
    refusal = parser.refuse_empty_string(question)
    
    assert refusal == NO_DATA

def test_should_remove_all_accented_characters():
    """
        Test of remove_accented_characters()
    """
    question = "Bonjour, @que peux-tu me dire à propos du musée # des <Confluences> à Lyon ?"
    cleaned_question = parser.remove_accented_characters(question)
    
    assert cleaned_question == "bonjour, @que peux-tu me dire a propos du musee # des <confluences> a lyon ?"
    
def test_should_remove_all_special_characters():
    """
        Test of remove_special_characters()
    """
    question = "bonjour, @que peux-tu me dire, l'ami, a propos du musee # des <confluences> a lyon ?"
    cleaned_question = parser.remove_special_characters(question)
    
    assert cleaned_question == "bonjour que peux-tu me dire ami a propos du musee  des confluences a lyon "

def test_should_keep_relevent_part_regex_ok():
    """
        Test of keep_relevent_part(), case 1
        Regex are effective on the string
    """
    question = "bonjour que peux-tu me dire ami a propos du musee  des confluences a lyon "
    cleaned_question = parser.keep_relevent_part(question)
    
    assert cleaned_question == "musee  des confluences a lyon"
    
def test_should_keep_relevent_part_regex_have_no_effect():
    """
        Test of keep_relevent_part(), case 2
        Regex have no effect on the string
    """
    question = "bonjour que peux-tu me dire ami sur le musee des confluences a lyon"
    cleaned_question = parser.keep_relevent_part(question)
    
    assert cleaned_question == "bonjour que peux-tu me dire ami sur le musee des confluences a lyon"

def test_should_get_cleaned_data_list():
    """
        Test of get_cleaned_data_list()
    """
    question = "musee  des confluences a lyon"
    cleaned_data_list = parser.get_cleaned_data_list(question)
    
    assert cleaned_data_list.sort() == ['musee', 'des', 'confuences', 'a', 'lyon'].sort()
    
def test_should_remove_all_stop_words():
    """
        Test of remove_stopwords()
    """
    cleaned_data_list = ['musee', 'des', 'confuences', 'a', 'lyon']
    cleaned_stopwords_list = ['des', 'a']
    
    parsed_question = parser.remove_stopwords(cleaned_data_list, cleaned_stopwords_list)
    
    assert parsed_question.sort() == ['musee', 'confuences', 'lyon'].sort()
    
def test_should_get_cleaned_string(monkeypatch):
    """
        Test of get_cleaned_string(), case 1
        Nominal case
    """
    question = "Bonjour, @que peux-tu me dire à propos du musée # des <Confluences> à Lyon ?"
    
    def mock_remove_accented_characters(string):
        return "bonjour, @que peux-tu me dire a propos du musee # des <confluences> a lyon ?"

    def mock_remove_special_characters(string):
        return "bonjour que peux-tu me dire a propos du musee  des confluences a lyon "

    def mock_keep_relevent_part(string):
        return "musee  des confluences a lyon "

    def mock_get_cleaned_data_list(string):
        return ['musee', 'des', 'confluences', 'a', 'lyon']

    def mock_get_clean_stopwords_list():
        return ['des', 'a']

    def mock_remove_stopwords(list1, list2):
        return ['musee', 'confluences', 'lyon']

    monkeypatch.setattr(parser, 'remove_accented_characters', mock_remove_accented_characters)
    monkeypatch.setattr(parser, 'remove_special_characters', mock_remove_special_characters)
    monkeypatch.setattr(parser, 'keep_relevent_part', mock_keep_relevent_part)
    monkeypatch.setattr(parser, 'get_cleaned_data_list', mock_get_cleaned_data_list)
    monkeypatch.setattr(parser, 'get_clean_stopwords_list', mock_get_clean_stopwords_list)
    monkeypatch.setattr(parser, 'remove_stopwords', mock_remove_stopwords)
        
    cleaned_question = parser.get_cleaned_string(question)

    assert set(cleaned_question.split()) == set('musee confluences lyon'.split())
    
def test_should_get_no_data_response_because_empty_or_spaces_string():
    """
        Test of get_cleaned_string(), case 2
        The string is empty or consisting solely of spaces
    """
    question = ""
    
    def mock_refuse_empty_string(string):
        return NO_DATA

    parser.refuse_empty_string = mock_refuse_empty_string
    cleaned_question = parser.get_cleaned_string(question)

    assert cleaned_question == NO_DATA
