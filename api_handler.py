import requests

class ApiHandler:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

    def assert_status_code(self, expected, received, url, response):
        assert expected == received, f'Bad status code. ' \
        f'"Expected {expected}. Actual status code: {received}.' \
        f'URL: {url}. Response: {response}'

    def get_request(self, url, params, expected_status_code=200):

        try:
            response = requests.get(url=url, params=params, headers=self.headers)
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
        rs_json = response.json()
        self.assert_status_code(url=url, received=response.status_code, expected=expected_status_code, response=rs_json)

        return rs_json