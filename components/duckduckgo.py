from typing import Any, Dict, List, NewType, Optional
import json
import re
import bs4
import requests
import logging

INFOBOX_REGEX = re.compile("\[(.+)\]")

class DuckDuckGo:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        _ddg_url = f"https://api.duckduckgo.com/?q=&format=json"
        self._INFOBOX_REGEX = re.compile("\[(.+)\]")

    def search(self, question: str):
        """Fetch a DDG API url -- expects x-javascript responses"""

        ddg_search = f"https://api.duckduckgo.com/?q={question}&format=json"
        data = requests.get(ddg_search)
        if  (data.status_code == 200):
            search_result = json.loads(data.text)
            url = self.get_infobox_url(search_result)
            if url is None:
                url = self.get_first_url(search_result)
            self.logger.debug(f'Url For {question} is {url}. Source DDG')
            return url
        else:
            self.logger.debug(f'Error When Requesting DDG Info for {question}...')
            return None

    def get_infobox_url(self, search_result):
        """Check for, and return the url from, the infobox section of a SearchResult"""

        infobox = search_result.get("Infobox")
        if infobox:
            infobox_content = infobox.get("content")
            if infobox_content:
                content_info: Dict[str, Any]
                for content_info in infobox_content:
                    if content_info.get("label") == "Website":
                        url = content_info.get("value")
                        match = self._INFOBOX_REGEX.search(url)
                        if match:
                            first_match = match.groups()[0]
                            return first_match
    def get_first_url(self, search_result):
        results = search_result.get('Results', [])
        if results:
            return results[0].get("FirstURL")
