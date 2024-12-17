def remove_outliers(prices_dict):
    prices = list(prices_dict.values())
    n = len(prices)
    
    if n == 0:
        return {}

    # Sort the prices
    prices.sort()

    # Calculate median
    if n % 2 == 1:
        median = prices[n // 2]
    else:
        median = (prices[n // 2 - 1] + prices[n // 2]) / 2

    # Calculate the position for the number to the right of the median
    position = n // 2 + n // 5
    if position >= n:
        position = n - 1  # Ensure the position is within bounds

    reference_price = prices[position]

    # Calculate the upper and lower bounds for filtering outliers
    upper_bound = reference_price * 1.5
    lower_bound = median * 0.5

    print(f"Median: {median}")
    print(f"Reference price: {reference_price}")
    print(f"Lower bound: {lower_bound}")
    print(f"Upper bound: {upper_bound}")

    # Filter the prices and add debugging statements
    filtered_prices_dict = {url: price for url, price in prices_dict.items() if lower_bound <= price <= upper_bound}

    print(f"Filtered prices: {filtered_prices_dict}")

    # Convert the filtered prices back to a list and sort it
    filtered_prices = sorted(filtered_prices_dict.values())

    # Remove a number from both the beginning and the end of the list for every ten items
    num_to_remove = len(filtered_prices) // 10
    if num_to_remove > 0:
        filtered_prices = filtered_prices[num_to_remove:-num_to_remove]

    # Reconstruct the filtered prices dictionary
    final_filtered_prices_dict = {url: price for url, price in filtered_prices_dict.items() if price in filtered_prices}

    print(f"Final filtered prices: {final_filtered_prices_dict}")

    return final_filtered_prices_dict