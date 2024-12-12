from urllib.parse import urlparse
import requests
import os

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')   
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')


def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    parts = domain.split('.')
    if parts[0] == 'www':
        parts = parts[1:]
    return '.'.join(parts) if domain else None


def perform_google_search(item_name, num_results):
    api_key = GOOGLE_API_KEY
    cse_id = GOOGLE_CSE_ID 
    query = f'shop {item_name}'
    urls = []

    for start in range(1, num_results + 1, 10): 
        url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&start={start}'
        response = requests.get(url)
        results = response.json()

        if 'items' not in results:
            break
        for item in results['items']:
            link = item['link']
            if link.startswith('https') and not \
                any(exclude in link for exclude in \
                    ['youtube', 'amazon', 'google', 'ebay', 'wiki', 'facebook', 
                     'twitter', 'instagram', 'pinterest', 'linkedin', 'reddit']):
                urls.append(link)

    return urls
