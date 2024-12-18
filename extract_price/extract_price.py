from playwright.async_api import async_playwright
from extract_price.filter_for_product_page import filter_for_product_page   
from extract_price.target_price import target_price, fetch_webpage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def extract_price(url_list):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # url_list = ['https://www.opticsplanet.com/armasight-collector-320-1-5-6x19mm-thermal-mini-weapon-sight.html']

        price_dict = {}
        for url in url_list:
            logger.info(f'{url_list.index(url) + 1}/{len(url_list)} Extracting price from {url}')
            page_content = fetch_webpage(url, timeout=10)
            if not page_content: 
                logger.debug('Error: Failed to fetch page content')
                continue

            try:
                await page.goto(url, timeout=6000)
                # Check if "This site can't be reached" is present in the page content
                if "This site can't be reached" in await page.content():
                    logging.error(f'Error: This site can\'t be reached')
                    continue
            except Exception as e:
                if "Protocol error (Page.navigate): Cannot navigate to invalid URL" in str(e):
                    continue
                logging.error(f'Error: {e}')    
                continue

            product_page = await filter_for_product_page(page)
            if not product_page:
                continue

            extracted_price = await target_price(page)
            if extracted_price is None:
                continue
            price_dict[url] = extracted_price

        await browser.close()

    # Sort the dictionary by value (price)
    sorted_price_dict = dict(sorted(price_dict.items(), key=lambda item: item[1]))
    logger.info(f'Prices extracted: {len(sorted_price_dict)}')

    return sorted_price_dict