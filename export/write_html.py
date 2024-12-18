import os
import sys

# Add the main directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resources.resources import extract_domain


def write_html(item_name, price_dict, output_file):
    with open(output_file, 'w') as f:
        f.write(f"<html>\n<head>\n<title>{item_name}</title>\n</head>\n<body>\n")
        f.write(f"<h1>{item_name}</h1>\n")
        f.write("<table border='1'>\n<tr><th>Competitor</th><th>Price</th></tr>\n")
        
        for url, price in price_dict.items():
            domain = extract_domain(url)
            formatted_price = f"${price:.2f}"
            f.write(f"<tr><td><a href='{url}' target='_blank'>{domain}</a></td><td>{formatted_price}</td></tr>\n")
        
        f.write("</table>\n</body>\n</html>")
