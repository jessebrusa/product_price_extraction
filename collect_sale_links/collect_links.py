import logging
import os
import sys

# Add the main directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import BASE_DIRECTORY
from resources.resources import perform_google_search, extract_domain
from difflib import SequenceMatcher
from collections import defaultdict
from urllib.parse import urlparse


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


default_num_results = 100


def filter_links(url_list, item_name):
    def url_in_competitors(url):
        domain = extract_domain(url)
        return domain in competitors_list

    file_path = os.path.join(BASE_DIRECTORY, 'collect_competitors', 
                             'competitors_list.txt')
    with open(file_path, 'r') as f:
        competitors_list = f.read().splitlines()

    competitor_check = False
    if competitor_check:
        filtered_url_list = []
        for url in url_list:
            if url_in_competitors(url):
                filtered_url_list.append(url)
    else:
        filtered_url_list = url_list
    if filtered_url_list:
        filtered_url_list = get_best_matches(item_name, filtered_url_list)
    else:
        print('No URLs found in competitors list.')

    if filtered_url_list:
        logger.info(f'Found {len(filtered_url_list)} competitors')

    return filtered_url_list


def group_urls_by_domain(urls):
    grouped_urls = defaultdict(list)
    for url in urls:
        domain = extract_domain(url)
        grouped_urls[domain].append(url)
    return grouped_urls


def get_best_matches(item_name, urls):
    grouped_urls = group_urls_by_domain(urls)
    best_matches = []
    for domain, domain_urls in grouped_urls.items():
        best_match = get_best_match(item_name, domain_urls)
        if best_match:
            best_matches.append(best_match)
    return best_matches
    

def get_best_match(item_name, urls, threshold=0.25):
    def match_ratio(item, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        return SequenceMatcher(None, item, path).ratio()

    best_match = None
    highest_ratio = 0
    for url in urls:
        ratio = match_ratio(item_name, url)
        if ratio < threshold:
            continue
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = url

    return best_match


if __name__ == "__main__":
    item_name = 'Armasight BNVD-51 Gen 3 Pinnacle Night Vision Goggle'
    urls = perform_google_search(item_name)
    filtered_urls = filter_links(urls, item_name)