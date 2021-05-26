#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests settings file
    To manage tests constants
"""

NO_MAP_DATA = []
RAW_MAP_DATA_OK = [
    {
        "title": "Musée des Confluences",
        "address": {
            "label": "Musée des Confluences, 69002 Lyon, France",
        },
        "position": {
            "lat": 45.73374,
            "lng": 4.81744
        }
    },
    {
        "title": "Musée des Confluences",
        "address": {
            "label": "Musée des Confluences, 28 Boulevard des Belges, 69006 Lyon, France",
        },
        "position": {
            "lat": 45.77449,
            "lng": 4.84819
        }
    }
]

NON_RELEVANT_MAP_DATA = [
    {
        "title": "Rue des Champs, Lyon, France",
        "address": {
            "label": "Rue des Champs, Lyon, France",
        },
        "position": {
            "lat": 48.84338,
            "lng": 2.33129
        }
    }
]
