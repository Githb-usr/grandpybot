#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests settings file
    To manage tests constants
"""

NO_MAP_DATA = []
NO_WIKI_DATA = []
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

RAW_WIKI_DATA_PAGE_TITLE = "Cathédrale Notre-Dame de Paris"
RAW_WIKI_COORDINATES = {
    "lat": 48.853056,
    "lon": 2.349722
    }
RAW_WIKI_EXTRACT = "La cathédrale Notre-Dame de Paris, communément appelée Notre-Dame, est l'un des monuments les plus emblématiques de Paris et de la France. Elle est située sur l'île de la Cité et est un lieu de culte catholique, siège de l'archidiocèse de Paris, dédiée à la Vierge Marie.\nCommencée sous l'impulsion de l'évêque Maurice de Sully, sa construction s'étend sur plus de deux siècles, de 1163 au milieu du XIVe siècle. Après la Révolution française, la cathédrale bénéficie entre 1845 et 1867 d'une importante restauration, parfois controversée, sous la direction de l'architecte Eugène Viollet-le-Duc, qui y incorpore des éléments et des motifs inédits. Pour ces raisons, le style n'est pas d'une uniformité totale : la cathédrale possède des caractères du gothique primitif et du gothique rayonnant. Les deux rosaces qui ornent chacun des bras du transept sont parmi les plus grandes d'Europe.\nElle est liée à de nombreux épisodes de l'histoire de France. Église paroissiale royale au Moyen Âge, elle accueille l'arrivée de la Sainte Couronne en 1239, puis le sacre de Napoléon Ier en 1804, le baptême d'Henri d'Artois, le duc de Bordeaux, en 1821, ainsi que les funérailles de plusieurs présidents de la..."
RAW_WIKI_PAGE_TITLE_AND_COORDINATES = {
    "title": "Quai de la Gironde",
    "lat": 48.8965,
    "lon": 2.383164
}
