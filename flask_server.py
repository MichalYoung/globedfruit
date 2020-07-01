"""
Display poetry with dynamically revealed translation.
Poetry source is marked up in a simple plain-text format,
which is converted when the page is served.
"""
import config

import tr_line  # Where we transform source text

import flask
from flask import request
from flask import jsonify
from flask import g
import zipfile
import logging

from typing import List

###
# Globals
###
app = flask.Flask(__name__)

import uuid

app.secret_key = str(uuid.uuid4())
app.debug = config.DEBUG
app.logger.setLevel(logging.DEBUG)
log = app.logger

##############
# URL routing
###############

@app.route("/")
def index():
    log.debug("invoked index")
    return flask.render_template("index.html")

@app.route("/neruda")
def neruda():
    return flask.render_template("nada_mas.html")

@app.route("/attempt")
def nada_mas():
    # This code is not working ... needs
    # complete rework
    log.debug("invoked /neruda")
    f = open("data/nada_mas.txt")
    log.debug("Opened")
    neruda = f.readlines()
    log.debug("Read the file")
    g.converted = tr_line.convert(neruda)
    log.debug("Converted")
    return flask.render_template("translation.html")

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
# EXAMPLE
# @app.route("/_suggest_completions")
# def suggest_completions():
#     """
#     Up to k suggestions for completing a word
#     """
#     app.logger.debug("Got a JSON request")
#     prefix = request.args.get('prefix', "default", type=str)
#     app.logger.debug(f"Prefix: '{prefix}")
#     app.logger.debug(f"The request object: {request}")
#     app.logger.debug(f"The arguments: '{request.args}")
#     if prefix:
#         app.logger.debug(f"Looking up '{prefix}' in {len(WORDLIST)} words")
#         completions = get_completions(prefix, 5)
#         app.logger.debug(f"Found completions {completions}")
#     else:
#         app.logger.debug("Didn't have a prefix to look up")
#         completions = []
#     return jsonify(suggestions=completions)


#############
# Used by request handlers
#############

# None

#############
#  Startup
#############

if __name__ == "__main__":
    import uuid

    app.secret_key = str(uuid.uuid4())
    app.debug = config.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=config.PORT)


