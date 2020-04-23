from components.dns_over_wikipedia import Dns_Over_Wikipedia
from components.certificate_transparency_logs import certificate_logs
import logging 
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)
crt_query = certificate_logs()

wikipedia_item = Dns_Over_Wikipedia(['pfizer', 'bbc', 'epic games','jackbox'])
data = wikipedia_item.find_domains()
for item in data:
    print(item['company_website'])
    #data = crt_query.perform_request(item['company_website'])
    certificate_urls = []
    if data is not None:
        print(data)
        crt_results = crt_query.perform_request(item['company_website'].lower())
        print(crt_results)
