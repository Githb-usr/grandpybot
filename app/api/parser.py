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
        self.cleaned_data = ''
        self.parsed_data_list = []

    def remove_accented_characters(self, raw_data):
        """
            String cleaning to facilitate comparisons, step 1
            :param: raw_data is a string
            :return: a string without accented characters and in lower case
            :rtype: string
            Example : "Mémé réclame à boire !" --> "meme reclame a boire !"
        """
        # We replace the accented characters and use lower case
        no_accent_data = ''.join(
            (c for c in unicodedata.normalize('NFD', raw_data)
             if unicodedata.category(c) != 'Mn')
            )

        return no_accent_data.lower()

    def remove_special_characters(self, raw_data):
        """
            String cleaning to facilitate comparisons, step 2
            :param: raw_data is a string
            :return: a string without special characters
            :rtype: string
            Example : "who #are you?" --> "who are you"
        """
        no_accent_data = self.remove_accented_characters(raw_data)
        # We delete the special characters
        return re.sub(r'[^\w\s]','',no_accent_data)

    def get_cleaned_data_list(self, raw_data):
        """
            Cutting the string into words
            :param: raw_data is a string
            :return: a list containing all the words of the given string
            :rtype: list
        """
        # We remove any accents and special characters (punctuation and others)
        no_spe_char_data = self.remove_special_characters(raw_data)

        # We transform the string into a list of words
        cleaned_data_list = []
        cleaned_data_list = no_spe_char_data.split(' ')
        # We delete the duplicates
        cleaned_data_list = list(set(cleaned_data_list))
        # We delete the empty items
        cleaned_data_list = list(filter(('').__ne__, cleaned_data_list))

        return cleaned_data_list

    def remove_stopwords(self, raw_data):
        """
            Removal of unnecessary words from a pre-defined list
            :param: raw_data is a string
            :return: a list containing only the important words
            :rtype: list
        """
        # We get the original cleaned word list
        cleaned_data_list = self.get_cleaned_data_list(raw_data)

        # Accented characters are removed from the Stopwords list
        clean_stopwords = []
        for word in STOPWORDS:
            clean_word = self.remove_accented_characters(word)
            clean_stopwords.append(clean_word.strip())

        # We delete the duplicates
        clean_stopwords = list(set(clean_stopwords))
        # We determine the list of words to delete in the original list
        words_to_remove = list(set(cleaned_data_list) & set(clean_stopwords))

        # We remove unnecessary words from the original list
        for word in words_to_remove:
            cleaned_data_list.remove(word)

        self.parsed_data_list = cleaned_data_list

        return self.parsed_data_list

    def get_cleaned_data(self, raw_data):
        """
            Reconstruction of a string from the list of important words
            :param: raw_data is a string
            :return: a parsed/cleaned string without accents, special
            charatcters or unnecessary words
            :rtype: string
        """
        # A tuple is retrieved from the list of filtered words
        parsed_data = tuple(self.remove_stopwords(raw_data))
        # we reconstitute a string from the tuple
        self.cleaned_data = ' '.join(parsed_data)

        return self.cleaned_data
