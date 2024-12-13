from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup, NavigableString
import re

def find_price_element(element):
    while element:
        if "$" in element.get_text():
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
        print("Product is discontinued")
        print(page.url)
        return None
    
    # Find the first element containing "Add to Cart" or "Sold out" text
    element = soup.find(string=lambda text: isinstance(text, NavigableString) and ("add to cart" in text.lower() or "sold out" in text.lower()))
    
    if element:
        if "sold out" in element.lower():
            print(f"Found element with text: {element}")
            print(page.url)
            print(element.parent)
            print()
        return element.parent
    else:
        # If not found by text, search for input elements with value attribute
        element = soup.find("input", {"value": lambda value: value and "add to cart" in value.lower()})
        if element:
            print(f"Found input element with value: {element}")
            return element.parent
        else:
            # Search for button elements with "Add To Cart" or "Sold out" text
            element = soup.find("button", string=lambda text: isinstance(text, NavigableString) and ("add to cart" in text.lower() or "sold out" in text.lower()))
            if element:
                if "sold out" in element.lower():
                    print(f"Found button element with text: {element}")
                    print(page.url)
                return element
            else:
                # Search for span elements with "Add To Cart" text within buttons
                element = soup.find("button span", string=lambda text: isinstance(text, NavigableString) and "add to cart" in text.lower())
                if element:
                    print(f"Found span element with text: {element}")
                    return element.parent
                else:
                    return None

def extract_price(element):
    # First, try to find the price within the <div class="price--main"> tag
    main_price_element = element.find('div', class_='price--main')
    if main_price_element:
        text = main_price_element.get_text()
        match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
        if match:
            return match.group()
    
    # If no <div class="price--main"> tag is found, try to find the price within the <div class="price__current"> tag
    current_price_element = element.find('div', class_='price__current')
    if current_price_element:
        text = current_price_element.get_text()
        match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
        if match:
            return match.group()
    
    # If no specific price tags are found, try to find the price within the <span class="Details_actual-price"> tag
    actual_price_element = element.find('span', class_='Details_actual-price')
    if actual_price_element:
        text = actual_price_element.get_text()
        match = re.search(r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
        if match:
            return match.group()
    
    # If no specific price tags are found, fall back to the original method
    text = element.get_text()
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
        print("Add to cart element not found")
        print(page.url)
        print()
        return None
    
    # print()
    # print(page.url)
    # print(add_to_cart_element)
    # print()

    # Step 2: Find the price element
    price_element = find_price_element(add_to_cart_element)
    if not price_element:
        print("Price element not found")
        print(page.url)
        print()
        return None
    
    # print()
    # print(page.url)
    # print(price_element)
    # print()
    
    # Step 3: Extract the price
    price = extract_price(price_element)
    if not price:
        print("Price not found")
        print(page.url)
        print()
        return None

    # Step 4: Clean the extracted price
    cleaned_price = clean_price(price)


    return cleaned_price