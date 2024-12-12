def filter_out_category(page):
    categories = ['best sellers', 'low to high', 'high to low']
    for category in categories:
        if category in page.content():
            return True
    return False


def filter_out_blog(page):
    blog_indicators = ['article', 'publisher', 'author']
    for indicator in blog_indicators:
        if indicator in page.content():
            return True
    return False


def filter_for_product_page(page):
    if filter_out_category(page):
        return False
    # if filter_out_blog(page):
    #     return False
    return True