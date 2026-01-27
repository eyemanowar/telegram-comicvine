import requests

class ApiHandler:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

    def assert_status_code(self, url):
        assert self.status_code == self.expected_status_code, f'Bad status code. ' \
        f'"Expected {self.expected_status_code}. Actual status code: {self.status_code}.' \
        f'URL: {url}. Response: {self.rs_json}'

    def get_request(self, url, params, expected_status_code=200):

        try:
            response = requests.get(url=url, params=params, headers=self.headers)
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
        self.status_code = response.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = response.json()
        self.assert_status_code(url=url)

        return self.rs_json