#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata

from config.settings import STOPWORDS

class Parser:
    """
        Parser class
        To manage user question parsing
    """
    def __init__(self):
        """ Constructor """
        self.cleaned_string = ''
        self.cleaned_string_words_list = []

    def remove_accented_characters(self, raw_string):
        """
            String cleaning to facilitate comparisons, step 1
            :param: raw_string is a string
            :return: a string without accented characters and in lower case
            :rtype: string
            Example : "Mémé réclame à boire !" --> "meme reclame a boire !"
        """
        # We replace the accented characters and use lower case
        no_accent_data = ''.join(
            (c for c in unicodedata.normalize('NFD', raw_string)
             if unicodedata.category(c) != 'Mn')
            )

        return no_accent_data.lower()

    def remove_special_characters(self, raw_string):
        """
            String cleaning to facilitate comparisons, step 2
            :param: raw_string is a string
            :return: a string without special characters
            :rtype: string
            Example : "l'horloge de# no$tre-dame tourne ?" --> "horloge de notre-dame tourne"
        """
        # We delete the letters with quote (l', d', etc.)
        no_quote_letter_data = re.sub("(\s[a-z])'", " ", raw_string)
        # We delete the special characters except the hyphen
        return re.sub(r'[^\-\w\s]','',no_quote_letter_data)
    
    def keep_relevent_parts(self, raw_string):
        """
            String cleaning to facilitate comparisons, step 3
            :param: raw_string is a string
            :return: a string xxx
            :rtype: string
            Example : "xxx" --> "xxx"
        """        

    def get_cleaned_data_list(self, raw_string):
        """
            Cutting the string into words
            :param: raw_string is a string
            :return: a list containing all the words of the given string
            :rtype: list
        """
        # We transform the string into a list of words
        cleaned_data_list = []
        cleaned_data_list = raw_string.split(' ')
        # We delete the duplicates
        cleaned_data_list = list(set(cleaned_data_list))
        # We delete the empty items
        cleaned_data_list = list(filter(('').__ne__, cleaned_data_list))

        return cleaned_data_list

    def remove_stopwords(self, raw_list):
        """
            Removal of unnecessary words from a pre-defined list
            :param: cleaned_data_list is a list of cleaned words (strings)
            :return: a list containing only the important words
            :rtype: list
        """
        # Accented characters are removed from the Stopwords list
        clean_stopwords = []
        for word in STOPWORDS:
            clean_word = self.remove_accented_characters(word)
            clean_stopwords.append(clean_word.strip())

        # We delete the duplicates
        clean_stopwords = list(set(clean_stopwords))
        # We determine the list of words to delete in the original list
        words_to_remove = list(set(raw_list) & set(clean_stopwords))

        # We remove unnecessary words from the original list
        for word in words_to_remove:
            raw_list.remove(word)

        self.cleaned_string_words_list = raw_list

        return self.cleaned_string_words_list

    def get_cleaned_string(self, raw_string):
        """
            Reconstruction of a string from the list of important words
            :param: raw_string is a raw string to parse
            :return: a parsed/cleaned string without accents, special
            charatcters or unnecessary words
            :rtype: string
        """
        # We remove any accents and special characters (punctuation and others)
        no_accent_data = self.remove_accented_characters(raw_string)
        no_special_characters_data = self.remove_special_characters(no_accent_data)
        # We get the original cleaned word list
        cleaned_data_list = self.get_cleaned_data_list(no_special_characters_data)
        # A tuple is retrieved from the list of filtered words
        cleaned_string_words_list = tuple(self.remove_stopwords(cleaned_data_list))
        # we reconstitute a string from the tuple
        cleaned_string = ' '.join(cleaned_string_words_list)

        return cleaned_string
