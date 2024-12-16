from urllib.parse import urlparse
import os
import time
from playwright.sync_api import sync_playwright

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')   
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')
# print(GOOGLE_API_KEY)
# print(GOOGLE_CSE_ID)


def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    parts = domain.split('.')
    if parts[0] == 'www':
        parts = parts[1:]
    return '.'.join(parts) if domain else None


# def perform_google_search(item_name, num_results=100):
#     api_key = GOOGLE_API_KEY
#     cse_id = GOOGLE_CSE_ID 
#     query = f'shop {item_name}'
#     urls = []

#     # Get the directory of the current script
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     exclude_list_path = os.path.join(script_dir, 'exclude_list.txt')

#     for start in range(1, num_results + 1, 10): 
#         url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&start={start}'
#         response = requests.get(url)
        
#         if response.status_code != 200:
#             print(f"Error: Received status code {response.status_code}")
#             print(response.text)
#             break
        
#         results = response.json()

#         with open(exclude_list_path, 'r') as file:
#             exclude_list = file.readlines()
#             exclude_list = [url.strip() for url in exclude_list]

#         if not exclude_list:
#             exclude_list = []

#         if 'items' not in results:
#             print("No items found in the results")
#             break
        
#         for item in results['items']:
#             link = item['link']
#             if link.startswith('https') and not any(exclude in link for exclude in exclude_list):
#                 urls.append(link)

#     return urls


def perform_google_search(item_name, num_results=100):
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        query = f'shop {item_name}'
        search_url = f'https://www.google.com/search?q={query}'

        page.goto(search_url)

        for _ in range(num_results // 10):
            page.wait_for_selector('div#search a')
            links = page.query_selector_all('div#search a')
            for link in links:
                href = link.get_attribute('href')
                if href and href.startswith('https') and not any(exclude in href for exclude in exclude_list):
                    urls.append(href)
            next_button = page.query_selector('a#pnnext')
            if next_button:
                next_button.click()
                time.sleep(2)  # Wait for the next page to load
            else:
                break

        browser.close()

    return urls

