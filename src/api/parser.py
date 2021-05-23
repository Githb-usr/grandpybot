#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata

from config.settings import PARSER_REGEX, STOPWORDS, NO_DATA

class Parser:
    """
        Parser class
        To manage user question parsing
    """
    def __init__(self):
        """ Constructor """
        self.cleaned_string = ''
        self.cleaned_string_words_list = []
        
    def refuse_empty_string(self, raw_string):
        """
            We check that the user input value is not empty or made up of spaces
            :param: raw_string is a string
            :return: a string "no_data" indicating that the response is empty 
            or consists of spaces
            :rtype: string
        """
        trim_raw_string = raw_string.strip()
        if re.match(r"^(?![\s\S])", trim_raw_string):
            return NO_DATA

    def remove_accented_characters(self, raw_string):
        """
            String cleaning to facilitate comparisons, step 1
            :param: raw_string is a string
            :return: a string without accented characters and in lower case
            :rtype: string
            Example : "Mémé réclame à boire !" --> "meme reclame a boire !"
        """
        trimmed_string = raw_string.strip()
        # We replace the accented characters and use lower case
        no_accent_data = ''.join(
            (c for c in unicodedata.normalize('NFD', trimmed_string)
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
        no_quote_letter_data = re.sub(r"(\s[a-z])'", " ", raw_string)
        # We delete the special characters except the hyphen
        return re.sub(r'[^\-\w\s]','',no_quote_letter_data)
    
    def keep_relevent_parts(self, raw_string):
        """
            String cleaning to facilitate comparisons, step 3
            :param: raw_string is a string
            :return: a shorter string with the relevent part
            :rtype: string
            Example : "toi qui sait tout, dis-moi ou se trouve la gare de lyon
            à paris" --> "la gare de lyon a paris"
        """        
        regex_result = []
        # We apply the different predefined regex
        for regex in PARSER_REGEX:
            string = re.match(regex[0], raw_string)
            if string is not None:
                regex_result.append(string[regex[1]].strip())
                
        if not regex_result:
            return raw_string
        # regex_result being a list, we return only its content which is a string
        return regex_result[0]

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
        if self.refuse_empty_string(raw_string) == NO_DATA:
            print("La question de l'utilisateur est vide ou constituée d'espaces.")
            return NO_DATA
        
        # We remove any accents and special characters (punctuation and others)
        no_accent_data = self.remove_accented_characters(raw_string)
        no_special_characters_data = self.remove_special_characters(no_accent_data)
        # We apply the regex
        regex_result = self.keep_relevent_parts(no_special_characters_data)
        # We get the original cleaned word list
        cleaned_data_list = self.get_cleaned_data_list(regex_result)
        # A tuple is retrieved from the list of filtered words
        cleaned_string_words_list = tuple(self.remove_stopwords(cleaned_data_list))
        # we reconstitute a string from the tuple
        cleaned_string = ' '.join(cleaned_string_words_list)

        return cleaned_string
            
