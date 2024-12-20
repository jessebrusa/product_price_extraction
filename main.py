import asyncio
from collect_sale_links.collect_links import perform_google_search, filter_links
from extract_price.extract_price import extract_price 
from remove_outliers.remove_outliers import remove_outliers
from export.export import export_prices, sanitize_filename
import json
import logging
import os


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


skip_unfiltered = True
skip_competitor = True
skip_extract_price = False
skip_remove_outliers = False
skip_export = False
def main(item_name):
    if not skip_unfiltered:
        logger.info(f'Collecting links for "{item_name}"')
        unfiltered_link_list = perform_google_search(item_name, 100, headless=False)
        if not unfiltered_link_list:
            print(f'No search results found for "{item_name}"')
            return
        with open('./printout_data/unfiltered_links.txt', 'w') as file:
            for link in unfiltered_link_list:
                file.write(f'{link}\n')
    else:
        with open('printout_data/unfiltered_links.txt', 'r') as file:
            unfiltered_link_list = [line.strip() for line in file.readlines()]
            logger.info(f"Found {len(unfiltered_link_list)} URLs for \"{item_name}\"")

    if not skip_competitor:
        logger.info(f'Filtering links for "{item_name}"')
        competitor_link_list = filter_links(unfiltered_link_list, item_name)
        if not competitor_link_list:
            print('No competitors found')
            return
        with open('printout_data/competitor_links.txt', 'w') as file:
            for link in competitor_link_list:
                file.write(f'{link}\n')
    else:
        with open('printout_data/competitor_links.txt', 'r') as file:
            competitor_link_list = [line.strip() for line in file.readlines()]
        logger.info(f'Found {len(competitor_link_list)} competitors')

    if not skip_extract_price:
        logger.info(f'Extracting prices for "{item_name}"')
        price_dict = asyncio.run(extract_price(competitor_link_list))
        if not price_dict:
            print('No prices found')
            with open('printout_data/prices.json', 'w') as file:
                json.dump({'error': 'No prices found'}, file, indent=4)
            return
        with open('printout_data/prices.json', 'w') as file:
            json.dump(price_dict, file, indent=4)
    else:
        with open('printout_data/prices.json', 'r') as file:
            price_dict = json.load(file)
        logger.info(f'Prices extracted: {len(price_dict)}')
    
    if not skip_remove_outliers:
        filtered_price_dict = remove_outliers(price_dict)
        if not filtered_price_dict:
            print('No prices found')
            with open('printout_data/filtered_prices.json', 'w') as file:
                json.dump({'error': 'No prices found'}, file, indent=4)
            return
        with open('printout_data/filtered_prices.json', 'w') as file:
            json.dump(filtered_price_dict, file, indent=4)
    else:
        with open('printout_data/filtered_prices.json', 'r') as file:
            filtered_price_dict = json.load(file)
        logger.info(f"Final filtered prices: {len(filtered_price_dict)}")
    
    if not skip_export:
        export_dir = './export/export_files'
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        sanitized_item_name = sanitize_filename(item_name)
        export_prices(sanitized_item_name, filtered_price_dict, export_dir)


if __name__ == "__main__":
    # with open('collect_competitors/product_list.txt', 'r') as file:
    #     item_list = [line.strip() for line in file.readlines()] 
    # if item_list:
    #     for item_name in item_list:
    #         try:
    #             print(f'Processing "{item_name}"')
    #             main(item_name)
    #             print()
    #         except Exception as e:
    #             print(f'Error processing "{item_name}": {e}')

    item_name = 'ATN BlazeSeeker 210 Thermal Monocular'
    main(item_name)
