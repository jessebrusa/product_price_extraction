from playwright.sync_api import Page
from bs4 import BeautifulSoup
import re

def prioritize_price_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_elements = []

    # Extract relevant tags
    for tag in soup.find_all(['p', 'div', 'span', 'strong', 's', 'small', 'mark', 'data']):
        text = tag.get_text()
        # Filter by money symbols and exclude certain keywords and phone numbers
        if re.search(r'[\$\€\£]', text) and not re.search(r'(shipping|order|total|save|discount|off|tel:|list price|starting at)', text, re.IGNORECASE):
            # Exclude elements with specific classes or IDs
            if not tag.find_parent(class_='save-amount-wrap'):
                # Exclude elements with "List" or "list" in the same span or right before
                if not (tag.find_previous_sibling(text=re.compile(r'list', re.IGNORECASE)) or re.search(r'list', text, re.IGNORECASE)):
                    price_elements.append(tag)

    return price_elements

def prioritize_prices(price_elements):
    prioritized_prices = []

    for element in price_elements:
        text = element.get_text()
        # Check for contextual clues
        if re.search(r'(current|sale|discount|now)\s*price', text, re.IGNORECASE):
            prioritized_prices.append(element)
        # Prioritize elements with specific classes or IDs
        elif 'price__current' in element.get('class', []):
            prioritized_prices.append(element)
        # Prioritize elements wrapped in <ins> tags
        elif element.find('ins'):
            prioritized_prices.append(element.find('ins'))
        # Prioritize elements with data-price or data-value attribute
        elif element.has_attr('data-price') or element.has_attr('data-value'):
            prioritized_prices.append(element)
        # Prioritize elements with data-price-amount attribute and data-price-type="finalPrice"
        elif element.has_attr('data-price-amount') and element.get('data-price-type') == 'finalPrice':
            prioritized_prices.append(element)
        # Prioritize elements with complex price structures
        elif element.find('sup') and element.find('span'):
            prioritized_prices.append(element)
        # Prioritize elements with aria-label attribute containing price
        elif element.has_attr('aria-label') and re.search(r'[\$\€\£]', element['aria-label']):
            prioritized_prices.append(element)

    # If no prioritized prices found, return all price elements
    if not prioritized_prices:
        return price_elements

    return prioritized_prices

def clean_price(price_text):
    # Extract the numeric part of the price
    match = re.search(r'[\d,]+(?:\.\d{2})?', price_text)
    if match:
        price_cleaned = match.group(0).replace(',', '')
        try:
            return round(float(price_cleaned), 2)
        except ValueError:
            return None
    return None

def get_product_price(page: Page) -> float:
    html_content = page.content()
    price_elements = prioritize_price_tags(html_content)
    prioritized_prices = prioritize_prices(price_elements)

    for element in prioritized_prices:
        if element.find('sup') and element.find('span'):
            price_text = ''.join([e.get_text() for e in element.find_all(['sup', 'span'])])
        else:
            price_text = element.get_text().strip()
        
        if "List" in price_text:
            continue
        
        print(page.url)
        print(f"Extracted price text: {price_text}")  # Add this line to log the price text
        price = clean_price(price_text)
        if price is not None:
            return price

    return None