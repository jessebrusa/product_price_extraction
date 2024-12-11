from playwright.sync_api import sync_playwright
from urllib.parse import urlparse


def read_product_list(file_path):
    with open(file_path, 'r') as f:
        return f.read().splitlines()


def collect_competitor_links(product_list):
    competitors = set()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        for product in product_list:
            page.goto(f'https://www.google.com/search?q={product}')
            links = page.query_selector_all('a')
            count = 0
            for link in links:
                if count >= 50:
                    break
                href = link.get_attribute('href')
                if href and 'google' not in href and 'amazon' not in href and 'ebay' \
                                                not in href and 'youtube' not in href:
                    domain = urlparse(href).netloc
                    if domain and domain not in competitors:
                        competitors.add(domain)
                        count += 1
        browser.close()
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

    for competitor in competitors_list:
        if 'www.' in competitor:
            competitors_list[competitors_list.index(competitor)] = competitor[4:]

    competitors_list.sort()

    with open('./competitors_list.txt', 'w') as f:
        for competitor in competitors_list:
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


def main():
    product_list = read_product_list('./product_list.txt')
    competitors = collect_competitor_links(product_list)
    write_competitors_to_file(competitors, 'competitors_list.txt')


if __name__ == "__main__":
    main()