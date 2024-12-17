import asyncio
from collect_sale_links.collect_links import perform_google_search, filter_links
from extract_price.extract_price import extract_price 
from remove_outliers.remove_outliers import remove_outliers
import json
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
# item_name = 'Armasight BNVD-51 Gen 3 Pinnacle Night Vision Goggle'
# item_name = 'BOSS StrongBox 7126-7640 - Pull Out Drawer'
# item_name = 'Renogy 1.2kW Essential Kit'
# item_name = 'ATN BinoX 4T 384 1.25-5x Thermal Binoculars'
# item_name = 'Tuffy Security Products Underseat Drawer w/ Keyed Lock for Ford Explorer & Police Interceptor, 2011-2024, Black'
# item_name = 'PETLIBRO Dog Water Fountain, 2.1Gal/8L Capsule Dog Fountain for Medium to Large Dogs, Anti-Splash Dog Water Bowl Dispenser, Ultra-Quiet Pet Water Fountain Easy to Clean'


skip_unfiltered = False
skip_competitor = True
skip_extract_price = True
skip_remove_outliers = True
def main():
    logger.info(f'Collecting links for "{item_name}"')
    if not skip_unfiltered:
        unfiltered_link_list = perform_google_search(item_name, 100, headless=True)
        if not unfiltered_link_list:
            print(f'No search results found for "{item_name}"')
            return
        with open('./printout_data/unfiltered_links.txt', 'w') as file:
            for link in unfiltered_link_list:
                file.write(f'{link}\n')
    else:
        with open('printout_data/unfiltered_links.txt', 'r') as file:
            unfiltered_link_list = [line.strip() for line in file.readlines()]

    if not skip_competitor:
        competitor_link_list = filter_links(unfiltered_link_list, item_name)
        if not competitor_link_list:
            print('No competitors found')
            return
        with open('printout_data/competitor_links.txt', 'w') as file:
            for link in competitor_link_list:
                file.write(f'{link}')
    else:
        with open('printout_data/competitor_links.txt', 'r') as file:
            competitor_link_list = [line.strip() for line in file.readlines()]

    if not skip_extract_price:
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
    
    



if __name__ == "__main__":
    main()