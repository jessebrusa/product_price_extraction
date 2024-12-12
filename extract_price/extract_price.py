from playwright.sync_api import sync_playwright
from extract_price.filter_for_product_page import filter_for_product_page

def extract_price(url_list):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        price_dict = {}
        for url in url_list:
            page.goto(url) 
            product_page = filter_for_product_page(page)
            if product_page:
                print(f'product page found')
                price_dict[url] = 'price'
                continue
            print(f'Not a product page')

        browser.close()

    return price_dict

# Example usage
if __name__ == "__main__":
    extract_price("https://example.com")