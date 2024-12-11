import os 
import re


BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def extract_domain(url):
    match = re.search(r'https?://([^/]+)', url)
    if match:
        return match.group(1)
    return None