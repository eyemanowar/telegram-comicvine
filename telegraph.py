import requests
from dotenv import load_dotenv
import os

TELEGRAPH_API_KEY = os.getenv('TELEGRAPH_API_KEY')

class Telegraph:

    def __init__(self):
        self.tokken = TELEGRAPH_API_KEY
        self.title = "This week's releases"
        self.author = "John Doe"

    def make_post(self, json):
        page_response = requests.post("https://api.telegra.ph/createPage", data={
            "access_token": self.tokken,
            "title": self.title,
            "author_name": self.author,
            "content": str(json),
            "return_content": "true"
        })

        result = page_response.json()
        if result["ok"]:
            print("Post created successfully!")
            print("URL:", result["result"]["url"])
            return result
        else:
            print("Error:", result)