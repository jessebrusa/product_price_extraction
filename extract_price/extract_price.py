from playwright.async_api import async_playwright, TimeoutError
from extract_price.filter_for_product_page import filter_for_product_page   
from extract_price.target_price import target_price, fetch_webpage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def extract_price(url_list):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        price_dict = {}
        for url in url_list:
            logger.info(f'{url_list.index(url) + 1}/{len(url_list)} Extracting price from {url}')
            try:
                await page.goto(url, timeout=8000)
                # Check if "This site can't be reached" is present in the page content
                if "This site can't be reached" in await page.content():
                    logger.error(f'Error: This site can\'t be reached')
                    continue
            except Exception as e:
                if "Protocol error (Page.navigate): Cannot navigate to invalid URL" in str(e):
                    continue
                logger.error(f'Error: {e}')
                continue

            try:
                await page.wait_for_selector("body", timeout=10000)
            except TimeoutError:
                logger.error(f'Timeout while waiting for body element on page: {url}')
                continue

            try:
                extracted_price = await target_price(page)
                if extracted_price is not None:
                    price_dict[url] = extracted_price
            except Exception as e:
                logger.error(f'Error processing {url}: {e}')
                continue

        await browser.close()

    return price_dict