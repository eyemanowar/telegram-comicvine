from api_handler import ApiHandler
import json
import urllib.parse
import re
import requests
from dotenv import load_dotenv
import os

COMICVINE_API_KEY = os.getenv('COMICVINE_API_KEY')

class ComicVine:

    def __init__(self):
        self.api_key = COMICVINE_API_KEY
        self.content_for_telegraph_new_series = [
            {"tag": "b", "children": ["New series starting:"]},
        ]
        self.content_for_telegraph_continuous = [
            {"tag": "p", "children": []},
            {"tag": "hr", "children": ["• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •"]},
            {"tag": "b", "children": ["Continuous series"]}
        ]
        self.params = {
            'api_key': self.api_key,
            'format': 'json',
            # 'filter': f'store_date:2025-06-10|2025-06-11',
            'field_list': 'name,store_date,issue_number,volume,image,description',
            'sort': 'volume:asc'
        }
        self.url = 'https://comicvine.gamespot.com/api/issues/'
        self.api_handler = ApiHandler()

    @staticmethod
    def prep_content(self, comic):
        if not comic['description']:
            cleaned_description = 'No discription'
        else:
            cleaned_description = comic['description'].replace('</em>', ' ')
        description = re.sub(r'<[a-z]{1,6}>|<\/[a-z]{1,6}>', '', cleaned_description, flags=re.IGNORECASE)
        image = comic['image']['original_url']
        title = comic['volume']['name']
        issue_number = comic['issue_number']
        comic_content = [
            {"tag": "p", "children": []},
            {"tag": "hr", "children": ["• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •"]},
            {"tag": "b", "children": [f"{title} #{issue_number}"]},
            {"tag": "img", "attrs": {"src": image}},
            {"tag": "p", "children": [description]}
        ]
        return comic_content

    def get_new_issues(self, date):
        self.params['filter'] = f'store_date:{date[0]}|{date[1]}'
        data = self.api_handler.get_request(url=self.url,params=self.params)
        print(self.params)
        with open("hello1.json", "w") as my_file:
            json.dump(data, my_file, indent=4)
        with open('/Users/oleksiikol/Documents/ComicsHelper/database/database.json', 'r') as db_file:
            db = json.load(db_file)
            following_comics = db.keys()
        for comic in data['results']:
            comic_name = comic['volume']['name'].replace(":", ' -')
            if comic_name in following_comics:
                print(f'{comic['volume']['name']} is in reading list')
                self.content_for_telegraph_continuous += self.prep_content(self, comic)
            elif comic['issue_number'] == '1':
                print(f'{comic['volume']['name']} is a new series')
                self.content_for_telegraph_new_series += self.prep_content(self, comic)
            else:
                pass
        return json.dumps(self.content_for_telegraph_new_series + self.content_for_telegraph_continuous)