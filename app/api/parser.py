#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata
from config.settings import STOPWORDS

class Parser:
    """
        Parser class
        To manage questions parsing
    """
    def __init__(self):
        """ Constructor """
        self.parsed_data_string = ''
        self.parsed_data_list = []

    def remove_accented_characters(self, raw_data):
        # on vire les caractères accentués
        no_accent_data = ''.join((c for c in unicodedata.normalize('NFD', raw_data) if unicodedata.category(c) != 'Mn'))
        
        return no_accent_data.lower()
    
    def remove_special_characters(self, raw_data): 
        # on vire les caractères spéciaux
        return re.sub(r'[^\w\s]','',raw_data)

    def get_raw_data_list(self, raw_data):
        # on récupère la string sans accents
        no_accent_data = self.remove_accented_characters(raw_data)
        # on vire les éventuels caractères spéciaux (ponctuation et autres)
        no_spe_char_data = self.remove_special_characters(no_accent_data)

        raw_data_list = []
        # on sépare la string en liste de mots
        raw_data_list = no_spe_char_data.split(' ')
        raw_data_list = list(set(raw_data_list))
        raw_data_list = list(filter(('').__ne__, raw_data_list))
        raw_data_list

        return raw_data_list

    def remove_stopwords(self, raw_data):
        raw_data_list = self.get_raw_data_list(raw_data)
        clean_stopwords = []

        for word in STOPWORDS:
            clean_word = self.remove_accented_characters(word)
            clean_stopwords.append(clean_word.strip())

        clean_stopwords = list(set(clean_stopwords))
        deleted_words = list(set(raw_data_list) & set(clean_stopwords))

        for word in deleted_words:
            raw_data_list.remove(word)

        self.parsed_data_list = raw_data_list
        
        return self.parsed_data_list
    
    def get_parsed_data(self, raw_data):
        #on récupère un tuple à partir de la liste des mots filtrés
        parsed_data = tuple(self.remove_stopwords(raw_data))
        #on reconstitue une string
        self.parsed_data_string = ' '.join(parsed_data)

        return self.parsed_data_string
