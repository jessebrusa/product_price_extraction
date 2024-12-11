from googlesearch import search
import os
import sys

# Add the main directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import BASE_DIRECTORY, extract_domain
from difflib import SequenceMatcher
from urllib.parse import urlparse
from collections import defaultdict

default_num_results = 100

def perform_google_search(query, num_results=default_num_results):
    urls = []
    for url in search(query, num_results=num_results):
        urls.append(url)
    return urls

def collect_links(item_name):
    def url_in_competitors(url):
        file_path = os.path.join(BASE_DIRECTORY, 'collect_competitors', 'competitors_list.txt')
        with open(file_path, 'r') as f:
            competitors_list = f.read().splitlines()
        # print(f'Competitors list: {competitors_list}')
        domain = extract_domain(url)
        print(f'Extracted domain: {domain}')
        return domain in competitors_list

    if not isinstance(item_name, list):
        item_name = [item_name]

    url_list = []
    for item in item_name:
        urls = perform_google_search(f'shop {item}')
        print(f'Search results for "{item}": {urls}')
        for url in urls:
            if url_in_competitors(url):
                url_list.append(url)
                print(f'Found competitor: {url}')

    if url_list:
        url_list = get_best_matches(item_name, url_list)

    return url_list


def group_urls_by_domain(urls):
    grouped_urls = defaultdict(list)
    for url in urls:
        domain = urlparse(url).netloc
        grouped_urls[domain].append(url)
    return grouped_urls


def get_best_matches(item_name, urls):
    grouped_urls = group_urls_by_domain(urls)
    best_matches = []
    for domain, domain_urls in grouped_urls.items():
        best_match = get_best_match(item_name, domain_urls)
        if best_match:
            best_matches.append(best_match)
        print(f'{domain}: {best_match}')
    return best_matches
    

def get_best_match(item_name, urls):
    def match_ratio(item, url):
        return SequenceMatcher(None, item, url).ratio()

    best_match = None
    highest_ratio = 0
    for url in urls:
        ratio = match_ratio(item_name, url)
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = url

    return best_match


if __name__ == "__main__":
    item_name = "example_item"  # Replace with your actual item name
    competitor_link_list = collect_links(item_name)
    if not competitor_link_list:
        print("No competitors found")
    else:
        print(f"Competitor links: {competitor_link_list}")