#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from flask import Flask, request, redirect, url_for, render_template, jsonify
import os

from . import app
from app.errors import HereNetworkError, HereBadRequestError, HereJsonError, WikiNetworkError, WikiBadRequestError, WikiJsonError
from app.api.map_api import MapApi
from app.api.wiki_api import WikiApi
from config.settings import DEFAULT_COORDINATES, DEFAULT_TITLE, DEFAULT_EXTRACT, POSITIVE_GRANDPY_MESSAGES, NEGATIVE_GRANDPY_MESSAGES, DEFAULT_RESPONSE

@app.route('/')
def index():
    """
        Route to display the HTML page of the application
        :return: an HTML template
    """
    return render_template('index.html')

@app.route('/question', methods=['GET'])
def getQuestion():
    """
        Route for communication between Python and AJAX
        :return: JSON data converted to HTML response
        :rtype: HTML response
    """
    # We get the question from the user
    question = request.args.get('q')
    print("viexs", os.environ.get('PORT'))
    #Data are processed by Python
    wiki_object = WikiApi()
    try:
        wiki_data = wiki_object.get_first_complete_wiki_data(question)
    except (WikiNetworkError, WikiBadRequestError, WikiJsonError, HereNetworkError, HereBadRequestError, HereJsonError):
        print("Something went wrong (first step).")
        map_object = MapApi()
        try:
            map_coord = map_object.get_cleaned_map_data(question)
            wiki_data = wiki_object.get_second_complete_wiki_data(map_coord)
        except (WikiNetworkError, WikiBadRequestError, WikiJsonError, HereNetworkError, HereBadRequestError, HereJsonError):
            print("Something went wrong (second step).")
            return jsonify(DEFAULT_RESPONSE)
        else:
            response = {
                "map": map_coord,
                "wiki": wiki_data,
                "apiKey": os.environ.get('HERE_JS_API_KEY'),
                "default_title": DEFAULT_TITLE,
                "default_extract": DEFAULT_EXTRACT,
                "positive_messages": POSITIVE_GRANDPY_MESSAGES,
                "negative_messages": NEGATIVE_GRANDPY_MESSAGES
            }

            return jsonify(response)
    else:
        response = {
            "map": DEFAULT_COORDINATES,
            "wiki": wiki_data,
            "apiKey": os.environ.get('HERE_JS_API_KEY'),
            "default_title": DEFAULT_TITLE,
            "default_extract": DEFAULT_EXTRACT,
            "positive_messages": POSITIVE_GRANDPY_MESSAGES,
            "negative_messages": NEGATIVE_GRANDPY_MESSAGES
        }

        return jsonify(response)
