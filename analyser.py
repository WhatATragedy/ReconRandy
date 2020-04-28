from components.dns_over_wikipedia import Dns_Over_Wikipedia
from components.certificate_transparency_logs import certificate_logs
from components.dns_over_https import Dns_Over_Https
import json
import logging 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)
crt_query = certificate_logs()
doh = Dns_Over_Https()
final_dataset = []

wikipedia_item = Dns_Over_Wikipedia(['bbc','jackbox'])
wiki_data = wikipedia_item.find_domains()
for item in wiki_data:
    #data = crt_query.perform_request(item['company_website'])
    certificate_urls = []
    if wiki_data is not None:
        crt_results = crt_query.perform_request(item['company_website'].lower())
        responses = doh.doh_query(crt_results)
        item['responses'] = responses
        final_dataset.append(item)
with open('final_output,json', 'w') as output_file:
    json.dump(final_dataset, output_file)

