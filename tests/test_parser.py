#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src import Parser

parser = Parser()

def test_should_remove_all_accented_characters():
    question = 'bonjour où se trouve Ménélik ?'
    cleaned_question = parser.remove_accented_characters(question)
    
    assert cleaned_question == 'bonjour ou se trouve menelik ?'
    
def test_should_remove_all_special_characters():
    pass

def test_should_get_cleaned_data_list():
    pass

def test_should_remove_all_stop_words():
    question = 'bonjour ou se trouve strasbourg'
    no_accent_data = parser.remove_accented_characters(question)
    no_special_characters_data = parser.remove_special_characters(no_accent_data)
    cleaned_data_list = parser.get_cleaned_data_list(no_special_characters_data)
    parsed_question = parser.remove_stopwords(cleaned_data_list)
    
    assert len(parsed_question) == 2
    assert 'bonjour' in parsed_question
    assert 'strasbourg' in parsed_question
    
def test_should_get_cleaned_string():
    pass
