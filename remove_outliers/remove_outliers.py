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


    # Adjust the bounds for filtering outliers
    lower_bound = median * 0.35
    upper_bound = median * 1.65


    # Filter the prices and add debugging statements
    filtered_prices = {}
    for k, v in prices_dict.items():
        if lower_bound <= v <= upper_bound:
            filtered_prices[k] = v
        else:
            print(f"Filtered out: {k} with price {v}")

    return filtered_prices