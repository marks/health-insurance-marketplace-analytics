# import dependencies
import time
import datetime
import requests
import pandas as pd
import logging
import csv

# set up some logging
reload(logging) # per http://stackoverflow.com/a/21475297/252671
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s: [%(levelname)s]: %(message)s',level=logging.DEBUG)


# helper function
def get_json_from_url(url):
    try:
        logging.info("HTTP GET'ing: "+ url)
        r = requests.get(url)
        r = r.json()
    except:
        logging.debug("  Request Failed")
        r = {}
    # logging.debug(r)
    return r


array_of_index_files = [
    "https://fm.formularynavigator.com/jsonFiles/publish/11/47/cms-data-index.json",
    "https://www.deltadental.com/CMSDirectory/index.json",
    "https://api.humana.com/v1/cms/index.json",
]

all_drugs = []

# take a index.json file, fetch it
for index_url in array_of_index_files:
    logging.info("About to fetch index.json: {0}".format(index_url))
    index_json = get_json_from_url(index_url)
    
    # for all URLs in formulary_urls array, flatten into one array
    for formulary_url in index_json["formulary_urls"]:
        logging.info("About to fetch formulary.json: {0}".format(formulary_url))
        formulary_json = get_json_from_url(formulary_url)
        for drug in formulary_json:
            for plan in drug["plans"]:
            	drug_plan_dict = {
            		'_index_url': index_url,
            		'_formulary_url': formulary_url,
            		'rxnorm_id': drug.get('rxnorm_id'),
            		'drug_name': drug.get('drug_name')
            	}
            	drug_plan_dict.update(plan)
            	all_drugs.append(drug_plan_dict)

logging.debug('Saving all_drugs to all_drugs.json and all_drugs.csv')

# save to JSON
f = open('all_drugs.json', 'w')
print >> f, all_drugs
f.close()

# save to CSV
keys = all_drugs[0].keys()
with open('all_drugs.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_drugs)

quit()



#     # for all URLs in provider_urls array, flatten into one array
#     for provider_url in index_json["provider_urls"]:
#         logging.info("About to fetch providers.json: {0}".format(provider_url))
    
#     # for all URLs in plan_urls array, flatten into one array
#     for plan_url in index_json["plan_urls"]:
#         logging.info("About to fetch plans.json: {0}".format(plan_url))