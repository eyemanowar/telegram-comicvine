from api_handler import ApiHandler
from database_helper import DbHandler
# import json
import html
import re
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv('keys.env')
COMICVINE_API_KEY = os.getenv('COMICVINE_API_KEY')
db_path = os.getenv('DATABASE_PATH', 'reading_list.json')

class ComicVine:

    def __init__(self):
        self.api_key = COMICVINE_API_KEY
        self.params = {
            'api_key': self.api_key,
            'format': 'json',
            # 'filter': f'store_date:2025-06-10|2025-06-11',
            'field_list': 'name,store_date,issue_number,volume,image,description',
            'sort': 'volume:asc'
        }
        self.url = 'https://comicvine.gamespot.com/api/issues/'
        self.api_handler = ApiHandler()
        self.db_handler = DbHandler()
        self.db_handler.init_db()

    @staticmethod
    def prep_content(comic, compact=False):
        image_obj = comic.get('image')
        image = image_obj.get('original_url') if image_obj else None
        title = comic['volume']['name']
        issue_number = comic['issue_number']
        link = comic['volume']['site_detail_url']
        comic_content = [
            {"tag": "p", "children": []},
            {"tag": "hr", "children": ["• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •"]},
            {"tag": "b", "children": [f"{title} #{issue_number}"]},
        ]
        if image:
            comic_content.append({"tag": "figure", "children": [
                {"tag": "img", "attrs": {"src": image}},
                {"tag": "figcaption", "children": [
                    {"tag": "a", "attrs": {"href": link}, "children": [f'{title}']}
                ]}
            ]})
        if not compact:
            if not comic['description']:
                description = ''
            else:
                cleaned_description = comic['description'].replace('</em>', ' ')
                cleaned_description = html.unescape(cleaned_description)
                description = re.sub(r'<.*?>', '', cleaned_description, flags=re.IGNORECASE)
            comic_content += [{"tag": "p", "children": [description]}]
        return comic_content

    def get_new_issues(self, date, user_id):
        filter_mode = self.db_handler.get_filter_mode(user_id)
        content_for_telegraph_continuous = [
            {"tag": "b", "children": ["Continuous series:"]},
        ]
        content_for_telegraph_new_series = [
            {"tag": "p", "children": []},
            {"tag": "hr", "children": ["• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •"]},
            {"tag": "b", "children": ["New series starting:"]}
        ]
        self.params['filter'] = f'store_date:{date[0]}|{date[1]}'
        data = self.api_handler.get_request(url=self.url,params=self.params)
        # with open(db_path, 'r') as db_file:
        #     db = json.load(db_file)
        #     following_comics = db.keys()
        following_comics = self.db_handler.get_reading_list(user_id)
        if filter_mode == 'list_and_first':
            for comic in data['results']:
                comic_name = comic['volume']['name'].replace(":", ' -')
                if comic_name.lower() in following_comics:
                    logger.info(f'{comic['volume']['name']} is in reading list')
                    content_for_telegraph_continuous += self.prep_content(comic)
                elif comic['issue_number'] == '1':
                    logger.info(f'{comic['volume']['name']} is a new series')
                    content_for_telegraph_new_series += self.prep_content(comic)
                else:
                    pass
            return content_for_telegraph_continuous + content_for_telegraph_new_series

        elif filter_mode == 'list':
            for comic in data['results']:
                comic_name = comic['volume']['name'].replace(":", ' -')
                if comic_name.lower() in following_comics:
                    logger.info(f'{comic['volume']['name']} is in reading list')
                    content_for_telegraph_continuous += self.prep_content(comic)
            return content_for_telegraph_continuous

        elif filter_mode == 'first':
            content_for_telegraph_new_series = [
                {"tag": "b", "children": ["New series starting:"]}
            ]
            for comic in data['results']:
                if comic['issue_number'] == '1':
                    logger.info(f'{comic['volume']['name']} is a new series')
                    content_for_telegraph_new_series += self.prep_content(comic)

            return content_for_telegraph_new_series

        elif filter_mode == 'all':
            content_for_telegraph_all = [
                {"tag": "b", "children": ["All series this week:"]},
            ]
            for comic in data['results']:
                content_for_telegraph_all += self.prep_content(comic, compact=True)
            return content_for_telegraph_all