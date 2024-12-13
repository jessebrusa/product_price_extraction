from playwright.sync_api import sync_playwright
from extract_price.filter_for_product_page import filter_for_product_page
from extract_price.target_price import get_product_price

def extract_price(url_list):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        price_dict = {}
        for url in url_list:
            page.goto(url) 
            product_page = filter_for_product_page(page)
            if not product_page:
                continue
            extracted_price = get_product_price(page)
            if extracted_price is None:
                continue
            price_dict[url] = extracted_price


        browser.close()

    return price_dict

