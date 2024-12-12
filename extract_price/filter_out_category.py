def filter_out_category(page):
    categories = ['best sellers', 'low to high', 'high to low']
    for category in categories:
        if category in page.content():
            return True
    return False


def filter_out_blog(page):
    # List of HTML tags and classes that are more indicative of blog or news pages
    blog_indicators = [
        'article', 'header', 'footer', 'section', 'aside', 'nav',
        '.author', '.comments', '.post', '.blog', '.news', '.entry', '.meta'
    ]

    # Check for the presence of these tags or classes in the page content
    for indicator in blog_indicators:
        if page.query_selector(indicator):
            return True

    return False


def filter_for_product_page(page):
    if filter_out_category(page):
        return False
    if filter_out_blog(page):
        return False
    return True