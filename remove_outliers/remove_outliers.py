import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def remove_outliers(prices_dict):
    prices = list(prices_dict.values())
    n = len(prices)
    
    if n == 0:
        return {}

    # Sort the prices
    prices.sort()

    if n % 2 == 1:
        median = prices[n // 2]
    else:
        median = (prices[n // 2 - 1] + prices[n // 2]) / 2

    position = n // 2 + n // 5
    if position >= n:
        position = n - 1  

    reference_price = prices[position]

    upper_bound = reference_price * 1.5
    lower_bound = median * 0.5

    logger.debug(f"Median: {median}")
    logger.debug(f"Reference price: {reference_price}")
    logger.debug(f"Upper bound: {upper_bound}")
    logger.debug(f"Lower bound: {lower_bound}")

    filtered_prices_dict = {url: price for url, price in prices_dict.items() if lower_bound <= price <= upper_bound}

    logger.debug(f"Prices: {filtered_prices_dict}")

    filtered_prices = sorted(filtered_prices_dict.values())

    num_to_remove = len(filtered_prices) // 10
    if num_to_remove > 0:
        filtered_prices = filtered_prices[num_to_remove:-num_to_remove]

    final_filtered_prices_dict = {url: price for url, price in filtered_prices_dict.items() if price in filtered_prices}

    logger.info(f"Final filtered prices: {len(final_filtered_prices_dict)}")

    return final_filtered_prices_dict