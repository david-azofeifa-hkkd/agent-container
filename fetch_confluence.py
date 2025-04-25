import os
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

class ConfluenceFetch():
    def __init__(self, key: str, usr: str):
        self.key = key
        self.url = "https://hakkoda.atlassian.net/wiki/"
        self.auth = HTTPBasicAuth(f"{usr}", f"{key}")
        self.headers = {
            "Accept": "application/json"
        }

    def general_search(self, search: str, limit=None, headers=None) -> json:
        headers = {
            "Accept": "application/json"
        }

        query = {
        'cql': search,
        'limit': limit
        }

        response = requests.request(
        "GET",
        self.url + "/rest/api/search/",
        headers=self.headers,
        params=query,
        auth=self.auth
        )
        return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    def get_titles(self, headers=None) -> dict:
        response = requests.request(
            "GET",
            self.url + "/api/v2/pages",
            headers=self.headers,
            auth=self.auth
        )
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    def parse_body(self):
        pass

if __name__ == "__main__":
    load_dotenv()
    confluence_key = os.environ["CONFLUENCE_API_KEY"]
    confluence_user = os.environ["CONFLUENCE_USERNAME"]
    cf = ConfluenceFetch(confluence_key, confluence_user)
    print(cf.general_search("title ~ data"))
    