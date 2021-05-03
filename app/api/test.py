#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.api.wiki_api import WikiApi

if __name__ == "__main__":
    test = WikiApi()
    result = test.get_wikipedia_data('gare%20marseille')
    print(result)

