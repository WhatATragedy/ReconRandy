import requests
import json
import logging

class certificate_logs:
    def __init__(self, logger=None):
        self.base_url = "https://crt.sh/?q={}&output=json"
        self.logger = logger or logging.getLogger(__name__)

    def perform_request(self, domain):
        if 'www.' in domain:
            domain = domain.replace('www.', '')
        domain = domain.lower()
        domain = "%.{}".format(domain)
        url_to_query = self.base_url.format(domain)
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        req = requests.get(url_to_query, headers={'User-Agent': ua})
        self.logger.debug(f'Request to CRT performed for {domain}, status {req.status_code}')
        if req.ok:
            content = req.content.decode('utf-8')
            data = json.loads(content)
            return self.process_data(data)

    def process_data(self, data):
        certificate_urls = []
        for item in data:
            if '\n' in item['name_value']:
                domains = item['name_value'].split('\n')
                certificate_urls.extend(domains)
            else:
                certificate_urls.append(item['name_value'])
        return list(set(certificate_urls))