from components.dns_over_wikipedia import Dns_Over_Wikipedia
from components.certificate_transparency_logs import certificate_logs
from components.dns_over_https import Dns_Over_Https
from components.duckduckgo import DuckDuckGo
import json
import logging 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)
crt_query = certificate_logs()
doh = Dns_Over_Https()
ddg = DuckDuckGo()
final_dataset = []

#wikipedia_item = Dns_Over_Wikipedia(['bbc','jackbox', 'ipsen'])
#wiki_data = wikipedia_item.find_domains()
for item in ['bbc','jackbox', 'ipsen']: 
    url = ddg.search(item)
    if url is None:
        wikipedia_item = Dns_Over_Wikipedia(item)
        wiki_data = wikipedia_item.find_domains()
        for item in wiki_data:
            url = item['company_website']
    if url is not None:
        crt_results = crt_query.perform_request(url.lower())
        responses = doh.doh_query(crt_results)
        final_dataset.append(responses)
    else:
        logger.debug(f'Issue with {item}.. No URL..')

with open('testing.json', 'w') as output_file:
    json.dump(final_dataset, output_file)