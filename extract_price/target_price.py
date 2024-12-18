from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup, NavigableString
import re
import requests
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def fetch_webpage(url, headers=None, timeout=10):
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            logger.debug(f"Error: Received status code {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.debug(f"Error: {e}")
        return None


def find_price_element(element):
    currency_symbols = ["$", "€", "£", "¥", "₹", "₽", "₩", "₪", "₫", "฿", "₴", "₦"]
    while element:
        text = element.get_text()
        if any(symbol in text for symbol in currency_symbols):
            return element
        element = element.parent
    return None


async def find_add_to_cart(page: Page):
    # Wait for the page to load partially by waiting for any element
    await page.wait_for_selector("body", timeout=10000)
    
    # Get the page content
    content = await page.content()
    
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove script and style tags
    for script in soup(["script", "style", "template"]):
        script.decompose()
    
    # Check if "discontinued" is present in the page content
    if soup.find(string=lambda text: isinstance(text, NavigableString) and "discontinued" in text.lower()):
        logger.debug("Discontinued product")
        logger.debug(page.url)
        return None
    
    # Find the first element containing "Add to Cart" or "Sold out" text
    element = soup.find(string=lambda text: isinstance(text, NavigableString) and ("add to cart" in text.lower() or "sold out" in text.lower()))
    
    if element:
        if "sold out" in element.lower():
            logger.debug(page.url)
            logger.debug(element)
        return element.parent
    else:
        # If not found by text, search for input elements with value attribute
        element = soup.find("input", {"value": lambda value: value and "add to cart" in value.lower()})
        if element:
            return element.parent
        else:
            # Search for button elements with "Add To Cart" or "Sold out" text
            element = soup.find("button", string=lambda text: isinstance(text, NavigableString) and ("add to cart" in text.lower() or "sold out" in text.lower()))
            if element:
                if "sold out" in element.lower():
                    logger.debug(f"Found element with text 'sold out': {element}")
                return element
            else:
                # Search for span elements with "Add To Cart" text within buttons
                element = soup.find("button span", string=lambda text: isinstance(text, NavigableString) and "add to cart" in text.lower())
                if element:
                    logger.debug(f"Found element with text 'Add to Cart': {element}")
                    return element.parent
                else:
                    return None


def extract_price(element):
    # Helper function to check if "MSRP" is around the price
    def has_msrp_around(element):
        text = element.get_text()
        if "msrp" in text.lower():
            return True
        return False

    # First, try to find the price within the <ins> tag inside <p class="price">
    price_element = element.find('p', class_='price')
    if price_element:
        ins_element = price_element.find('ins')
        if ins_element:
            text = ins_element.get_text()
            match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
            if match:
                return match.group()

    # Check for WooCommerce price elements
    price_elements = element.find_all('span', class_='woocommerce-Price-amount')
    for price_element in price_elements:
        text = price_element.get_text()
        match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
        if match:
            return match.group()

    # If no <ins> tag is found, try other methods

    # Try to find the price within the <small class="bold_option_price_display"> tag with data-price attribute
    price_elements = element.find_all('small', class_='bold_option_price_display')
    for price_element in price_elements:
        if price_element.has_attr('data-price'):
            price = price_element['data-price']
            if price:
                return price

    # Try to find the price within the <div class="price--main"> tag
    main_price_element = element.find('div', class_='price--main')
    if main_price_element and not has_msrp_around(main_price_element):
        text = main_price_element.get_text()
        if "value" not in text.lower():
            match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
            if match:
                return match.group()
    
    # Try to find the price within the <div class="price__current"> tag
    current_price_element = element.find('div', class_='price__current')
    if current_price_element and not has_msrp_around(current_price_element):
        text = current_price_element.get_text()
        if "value" not in text.lower():
            match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
            if match:
                return match.group()
    
    # Try to find the price within the <span class="Details_actual-price"> tag
    actual_price_element = element.find('span', class_='Details_actual-price')
    if actual_price_element and not has_msrp_around(actual_price_element):
        text = actual_price_element.get_text()
        if "value" not in text.lower():
            match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
            if match:
                return match.group()
    
    # Try to find the price within the <div class="price sale-price"> tag
    sale_price_element = element.find('div', class_='price sale-price')
    if sale_price_element and not has_msrp_around(sale_price_element):
        text = sale_price_element.get_text()
        if "value" not in text.lower():
            match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
            if match:
                return match.group()
    
    # Fall back to the original method
    text = element.get_text()
    if "value" not in text.lower() and "msrp" not in text.lower():
        match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
        if match:
            return match.group()
    
    return None


def clean_price(price):
    cleaned_price = re.sub(r'[^\d.]', '', price)
    cleaned_price = float(cleaned_price) if cleaned_price else None
    if cleaned_price == 0:
        return None
    return cleaned_price


async def target_price(page: Page):
    # Step 1: Find the "Add to Cart" or "Sold Out" button
    add_to_cart_element = await find_add_to_cart(page)
    if not add_to_cart_element:
        logger.debug("Add to Cart element not found")
        logger.debug(page.url)
        return None

    # Step 2: Find the price element
    price_element = find_price_element(add_to_cart_element)
    if not price_element:
        logger.debug("Price element not found")
        logger.debug(page.url)
        return None
    
    
    # Step 3: Extract the price
    price = extract_price(price_element)
    if not price:
        logger.debug("Price not found")
        logger.debug(page.url)
        return None

    # Step 4: Clean the extracted price
    cleaned_price = clean_price(price)
    if not cleaned_price:
        logger.debug("Price could not be cleaned")
        logger.debug(page.url)
        return None


    return cleaned_price