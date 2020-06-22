from components.dns_over_wikipedia import Dns_Over_Wikipedia
from components.certificate_transparency_logs import certificate_logs
from components.dns_over_https import Dns_Over_Https
from components.duckduckgo import DuckDuckGo
from objects.company import Company
import json
import logging 
import pandas as pd
import time
import tqdm
import os

"""logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')"""
logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)
df = pd.read_csv('dns_over_http/FTSE_100.txt')
companies = df['Company_Name'].tolist()
data = []
#for company_name in tqdm.tqdm(companies):
for index,company_name in enumerate(companies):
    done = os.listdir('e:/Stuff/Code/dns_over_http/results/')
    print(f'Processing {index} out of {len(companies)}')
    if company_name not in done:
        print(f'Company {company_name} not done...')
        company_obj = Company(company_name)
        company_obj.get_domain()
        company_obj.get_crt_logs()
        company_obj.get_dns_for_domains()
        data.append({
            'Company_Name': company_obj.company_name,
            'Url': company_obj.domain,
            'DNS': company_obj.domains_and_dns
        })
        ##check if file exists
        
        with open(f'e:/Stuff/Code/dns_over_http/results/{company_name}', 'w') as output_file:
            temp_dict = {
                'Company_Name': company_obj.company_name,
                'Url': company_obj.domain,
                'DNS': company_obj.domains_and_dns 
            }
            json.dump(temp_dict, output_file)
        time.sleep(1)
    else:
        print(f'Company {company_name} already done...')

output_df = pd.DataFrame(data)

"""
crt_query = certificate_logs()
doh = Dns_Over_Https()
ddg = DuckDuckGo()
final_dataset = []

#wikipedia_item = Dns_Over_Wikipedia(['bbc','jackbox', 'ipsen'])
#wiki_data = wikipedia_item.find_domains()
for item in ['bbc','jackbox']: 
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
"""