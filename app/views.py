#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dotenv import dotenv_values
from flask import Flask, request, redirect, url_for, render_template, jsonify
from . import app
from app.api.wiki_api import WikiApi
from app.api.map_api import MapApi
from app.api.parser import Parser

config = dotenv_values(".env")

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
    #Data are processed by Python
    map_object = MapApi()
    map_coord = map_object.choose_answer(question)
    wiki_object = WikiApi()
    wiki_data = wiki_object.get_wikipedia_data(map_coord)
    # We create a dictionary containing the data we want to send to AJAX
    response = {
        "map": map_coord,
        "wiki": wiki_data,
        "apiKey": config['HERE_JS_API_KEY']
    }

    return jsonify(response)
