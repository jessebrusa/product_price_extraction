import os 
from urllib.parse import urlparse


BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    parts = domain.split('.')
    if parts[0] == 'www':
        parts = parts[1:]
    return '.'.join(parts) if domain else None
