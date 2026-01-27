import re
from datetime import datetime, timedelta
import urllib
import json
import requests
from comic_vine import ComicVine
from telegraph import Telegraph
from time_helper import Date

comicvine = ComicVine()
tg = Telegraph()
date = Date()

today = date.get_the_current_week()
print(today)
new_issues = comicvine.get_new_issues(today)
tg_post = tg.make_post(new_issues)