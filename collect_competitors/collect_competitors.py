import os
import sys

# Add the main directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from resources.resources import perform_google_search
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse


unwanted_domains = ['youtube', 'amazon', 'google', 'ebay', 'wiki', 'facebook', 
                    'twitter', 'instagram', 'pinterest', 'linkedin', 'reddit',
                    'ironclad']


def read_product_list(file_path):
    with open(file_path, 'r') as f:
        return f.read().splitlines()


def collect_competitor_links(product_list):
    competitors = set()
    for product in product_list:
        urls = perform_google_search(product)
        count = 0
        for url in urls:
            if count >= 50:
                break
            if not any(domain in url for domain in unwanted_domains):
                domain = urlparse(url).netloc
                if domain and domain not in competitors:
                    competitors.add(domain)
                    count += 1
    return competitors


def write_competitors_to_file(competitors, file_path):
    with open(file_path, 'a') as f:
        for competitor in competitors:
            f.write(f'{competitor}\n')


def order_competitors():
    competitors_list = read_product_list('./competitors_list.txt')

    if not competitors_list:
        print('No competitors found')
        return

    # Remove 'www.' prefix and duplicates
    competitors_set = set()
    for competitor in competitors_list:
        if 'www.' in competitor:
            competitor = competitor[4:]
        competitors_set.add(competitor)

    sorted_competitors_list = sorted(competitors_set)

    with open('./competitors_list.txt', 'w') as f:
        for competitor in sorted_competitors_list:
            f.write(f'{competitor}\n')


def test_links():
    with open('./competitors_list.txt', 'r') as f:
        competitors_list = f.read().splitlines()

    valid_competitors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        for competitor in competitors_list:
            try:
                page.goto(f'https://{competitor}', timeout=10000)
                if page.title():
                    valid_competitors.append(competitor)
            except Exception as e:
                print(f'Error accessing {competitor}: {e}')
        browser.close()

    with open('./competitors_list.txt', 'w') as f:
        for competitor in valid_competitors:
            f.write(f'{competitor}\n')


def clean_competitors():
    with open('./competitors_list.txt', 'r') as f:
        competitors_list = f.read().splitlines()

    filtered_competitors = set()

    for competitor in competitors_list:
        if not any(domain in competitor for domain in unwanted_domains):
            filtered_competitors.add(competitor)

    with open('./competitors_list.txt', 'w') as f:
        for competitor in sorted(filtered_competitors):
            f.write(f'{competitor}\n')


def main():
    item_name = 'Renogy 1.2kW Essential Kit'
    competitors = collect_competitor_links([item_name])
    print(competitors)
    write_competitors_to_file(competitors, './competitors_list.txt')
    order_competitors()
    clean_competitors()


if __name__ == "__main__":
    main()