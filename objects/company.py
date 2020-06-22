from components.dns_over_wikipedia import Dns_Over_Wikipedia
from components.certificate_transparency_logs import certificate_logs
from components.dns_over_https import Dns_Over_Https
from components.duckduckgo import DuckDuckGo
import logging

class Company:
    def __init__(self, company_name, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.company_name = company_name
        self.domains_associated = None
        self.domains_and_dns = None
        self.wiki_page = None
        self.root_domain = None
        self.domain = url = None

    def get_domain(self):
        ddg = DuckDuckGo()
        url = ddg.search(self.company_name)
        if url is None:
            wikipedia_item = Dns_Over_Wikipedia(self.company_name)
            wiki_data = wikipedia_item.find_domains()
            for item in wiki_data:
                url = item['company_website']
        self.domain = url
        if self.domain is not None or not self.domain:
            self.find_root_domain(url)
            return self.domain
        else:
            return False

    def find_root_domain(self, url):
        if url is not None:
            if 'www.' in url:
                url = url.replace('www.', '')
            if 'http://' in url:
                url = url.replace('http://', '')
            if 'https://' in url:
                url = url.replace('https://', '')
            if '/' in url:
                url = url.split('/')[0]
            self.root_domain = url.lower()
            return self.root_domain
        else:
            return False

    def get_crt_logs(self):
        crt_query = certificate_logs()
        if self.root_domain is not None:
            self.domains_associated = crt_query.perform_request(self.root_domain)
            return self.domains_associated
        else:
            return None
        return None
        
    def get_dns_for_domains(self):
        doh = Dns_Over_Https()
        self.domains_and_dns = doh.doh_query(self.domains_associated)
        return self.domains_and_dns

        


