import requests
import json
import logging
from bs4 import BeautifulSoup

class Dns_Over_Wikipedia:
    def __init__(self, company_names, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.company_names = company_names if isinstance(company_names, list) else [company_names]
        self._api_prefix = 'https://en.wikipedia.org/w/api.php?action=query&prop=info&inprop=url&format=json&origin=*&titles='
        self.company_names_and_urls = []

    def find_domains(self): 
        for company_name in self.company_names:
            full_url = self.perform_info_request(company_name)
            if full_url is not None:
                urls = self.perform_wiki_page_request(full_url)
                for url in urls:
                    if "Official website" not in url:
                        self.company_names_and_urls.append({
                            'company_name': company_name,
                            'wikipedia_page': full_url,
                            'company_website': url
                        })
                        self.logger.debug(f'{company_name} and  {url}...')
            else:
                self.logger.debug(f'Error Processing {company_name}...')
        return self.company_names_and_urls

    def perform_info_request(self, company_name):   
        data = requests.get(self._api_prefix + company_name)
        if  (data.status_code == 200):
            page_info = json.loads(data.text)
            for page in page_info['query']['pages']:
                page_data =  page_info['query']['pages'][page]
                self.logger.debug(f"Page URL is {page_data['fullurl']}")
                return page_data['fullurl']
        else:
            self.logger.debug(f'Error When Requesting Wikipedia Info for {company_name}...')
            return None
            

    def perform_wiki_page_request(self, wikipedia_page):
        data = requests.get(wikipedia_page)
        urls = self.find_website_url_in_wiki_page(data.text)
        return urls

    def find_website_url_in_wiki_page(self, page_data):
        soup = BeautifulSoup(page_data, 'html.parser')
        urls = []
        spans = soup.find_all('span', {'class': 'url'})
        urls = set([span.get_text() for span in spans])
        return list(urls)

"""
self.company_names_and_urls.append({
'company_name': company_name,
'wikipedia_page': page_data['fullurl']
})"""