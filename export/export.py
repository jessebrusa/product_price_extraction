import os
import sys
import pandas as pd
import logging

# Add the main directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export.write_html import write_html

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def sanitize_data(data):
    sanitized_data = {}
    for key, value in data.items():
        sanitized_key = key.encode('ascii', 'ignore').decode('ascii')
        sanitized_value = str(value).encode('ascii', 'ignore').decode('ascii')
        sanitized_data[sanitized_key] = sanitized_value
    return sanitized_data

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def export_prices(item_name, price_dict, base_path, excel=True, json=True, html=True):  
    sanitized_price_dict = sanitize_data(price_dict)
    sanitized_item_name = sanitize_filename(item_name)

    # Convert prices to floats and sort the price_dict by price (value) from low to high
    sorted_price_dict = {k: float(v) for k, v in sorted(sanitized_price_dict.items(), key=lambda item: float(item[1]))}

    data = {'URL': list(sorted_price_dict.keys()), 'Price': list(sorted_price_dict.values())}
    df = pd.DataFrame(data)

    # Create a folder with the sanitized item name
    folder_path = os.path.join(base_path, sanitized_item_name).replace('\\', '/')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    logger.info(f'Exporting prices to {folder_path}')
    logger.debug(f'Prices: {df}')

    # Truncate the sheet name to 31 characters if necessary
    sheet_name = sanitized_item_name[:31]

    if excel:
        try:
            df.to_excel(os.path.join(folder_path, f'{sheet_name}.xlsx'), index=False, sheet_name=sheet_name)
            logger.info('Exported to Excel')
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")

    if json:
        try:
            df.to_json(os.path.join(folder_path, f'{sheet_name}.json'), orient='records', indent=4)
            logger.info('Exported to JSON')
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")

    if html:
        try:
            write_html(item_name, sorted_price_dict, os.path.join(folder_path, f'{sheet_name}.html'))
            logger.info('Exported to HTML')
        except Exception as e:
            logger.error(f"Error exporting to HTML: {e}")

    logger.info('Export complete')