from flask import Flask, jsonify, request
from comic_vine import ComicVine
from telegraph import Telegraph
from time_helper import Date

comicvine = ComicVine()
tg = Telegraph()
date = Date()

app = Flask(__name__)

@app.route('/api/date', methods=['GET'])
def get_current_week():
    return jsonify(date.get_the_current_week())

