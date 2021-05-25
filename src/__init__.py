from flask import Flask

app = Flask(__name__)

from . import views
from .api.map_api import MapApi
from .api.wiki_api import WikiApi
from .api.parser import Parser
