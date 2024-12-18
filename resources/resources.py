from urllib.parse import urlparse, quote
import os
import time
from playwright.sync_api import sync_playwright
import requests
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')   
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')


def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    parts = domain.split('.')
    if parts[0] == 'www':
        parts = parts[1:]
    return '.'.join(parts) if domain else None


def perform_google_search(item_name, num_results=100, headless=False, GOOGLE_API=False):
    urls = None
    if GOOGLE_API:
        urls = perform_google_search_api(item_name, num_results)
    else:
        urls = perform_google_search_playwright(item_name, num_results, headless)

    return urls


def perform_google_search_api(item_name, num_results=100):
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        logger.warning(f'GOOGLE_API_KEY: {GOOGLE_API_KEY}')
        logger.warning(f'GOOGLE_CSE_ID: {GOOGLE_CSE_ID}')

    api_key = GOOGLE_API_KEY
    cse_id = GOOGLE_CSE_ID 
    query = quote(f'shop {item_name}')
    urls = []

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exclude_list_path = os.path.join(script_dir, 'exclude_list.txt')

    for start in range(1, num_results + 1, 10): 
        url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&start={start}'
        logger.info(f'Performing search for "{item_name}"')
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
            break
        
        results = response.json()

        with open(exclude_list_path, 'r') as file:
            exclude_list = file.readlines()
            exclude_list = [url.strip() for url in exclude_list]

        if not exclude_list:
            exclude_list = []

        if 'items' not in results:
            print("No items found in the results")
            break
        
        for item in results['items']:
            link = item['link']
            if link.startswith('https') and not any(exclude in link for exclude in exclude_list):
                urls.append(link)

    return urls


def perform_google_search_playwright(item_name, num_results=100, headless=False):
    urls = []

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exclude_list_path = os.path.join(script_dir, 'exclude_list.txt')

    with open(exclude_list_path, 'r') as file:
        exclude_list = file.readlines()
        exclude_list = [url.strip() for url in exclude_list]

    if not exclude_list:
        exclude_list = []

    with sync_playwright() as p:
        logger.debug('Launching browser')
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        query = f'shop {item_name}'
        search_url = f'https://www.google.com/search?q={query}'

        logger.info(f'Performing search for "{query}"')
        page.goto(search_url)

        for i in range(num_results // 10):
            try:
                page.wait_for_selector('div#search a', state='attached', timeout=10000)
                logger.info(f'Search results loaded for page {i+1}')
                links = page.query_selector_all('div#search a')
                for link in links:
                    href = link.get_attribute('href')
                    if href and href.startswith('https') and not any(exclude in href for exclude in exclude_list):
                        urls.append(href)
                next_button = page.query_selector('a#pnnext')
                if next_button:
                    logger.debug('Clicking next button')
                    next_button.click()
                else:
                    break
            except Exception as e:
                logger.error(f'Error: {e}')
                break

        browser.close()

        if not urls:
            logger.warning(f"No search results found for \"{item_name}\"")
        else:
            logger.info(f"Found {len(urls)} URLs for \"{item_name}\"")
            logger.debug(f"URLs: {urls}")


    return urls
