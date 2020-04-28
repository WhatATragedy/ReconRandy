import json
import re
import socket
import ssl
import subprocess
import sys
import urllib.request
from typing import List
import logging

class Dns_Over_Https:
    def __init__(self, logger=None):
        self.DOH_SERVER = "cloudflare-dns.com"
        self._urlopen = urllib.request.urlopen
        self._Request = urllib.request.Request
        self.responses = []
        self.logger = logger or logging.getLogger(__name__)

    def doh_query(self, domains: List[str], qtypes: List[str]=None):
        url = "https://cloudflare-dns.com/dns-query?name={}&type={}"
        print(domains)
        domains = domains if isinstance(domains, list) else [domains]
        qtypes = qtypes if qtypes else ['A', 'AAAA']
        content_type = 'application/dns-json'
        headers = {"accept": content_type}
        urls = [url.format(domain, qtype) for domain in domains for qtype in qtypes]
        for url in urls:
            self.logger.debug(f'Request to CloudFlare DNS for {url}...')
            req = self._Request(url, headers=headers)
            content = self._urlopen(req).read().decode()
            self.logger.debug(f'Response {content}...')
            parsed = self.parse_response(json.loads(content))
            if parsed is not None:
                self.responses.extend(parsed)
        return self.responses

    def parse_response(self, response: str):
        domain_data = []
        if 'Answer' in response.keys():
            for item in response['Answer']:
                domain_data.append({
                    'question': item['name'],
                    'answer': item['data'],
                    'type': item['type']
                })
            self.logger.debug(f'Parsed Response {domain_data}...')
            return domain_data
        else:
            self.logger.debug(f'No answer for {response}...')
            return None



