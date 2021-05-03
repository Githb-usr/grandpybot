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
    return render_template('index_test.html', apikey=config['HERE_JS_API_KEY'])

@app.route('/question', methods=['GET'])
def getQuestion():
    question = request.args.get('q')
    map_object = MapApi()
    map_coord = map_object.choose_answer(question)
    wiki_object = WikiApi()
    wiki_data = wiki_object.get_wikipedia_data(map_coord)
    
    return jsonify(wiki_data)
