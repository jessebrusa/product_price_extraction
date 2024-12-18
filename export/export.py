import os
import sys

# Add the main directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export.write_html import write_html
import pandas as pd
import logging

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

def export_prices(item_name, price_dict, file_path, excel=True, json=True, html=True):  
    sanitized_price_dict = sanitize_data(price_dict)

    data = {'URL': list(sanitized_price_dict.keys()), 'Price': list(sanitized_price_dict.values())}
    df = pd.DataFrame(data)

    logger.info(f'Exporting prices to {file_path}')
    logger.debug(f'Prices: {df}')

    # Truncate the sheet name to 31 characters if necessary
    sheet_name = item_name[:31]

    if excel:
        try:
            df.to_excel(f'{file_path}.xlsx', index=False, sheet_name=sheet_name)
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")

    if json:
        try:
            df.to_json(f'{file_path}.json', orient='records', indent=4)
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")

    if html:
        try:
            write_html(item_name, price_dict, f'{file_path}.html')
        except Exception as e:
            logger.error(f"Error exporting to HTML: {e}")

    logger.info('Export complete')