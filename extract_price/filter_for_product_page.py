from playwright.async_api import Page

async def filter_out_category(page: Page) -> bool:
    categories = ['best sellers', 'low to high', 'high to low', 'sort by']
    content = await page.content()
    for category in categories:
        if category in content:
            return True
    return False

async def filter_out_blog(page: Page) -> bool:
    # Check for the presence of elements that are more unique to blogs
    blog_indicators = [
        '.author',
    ]

    for indicator in blog_indicators:
        if await page.query_selector(indicator):
            return True

    return False

async def filter_for_product_page(page: Page) -> bool:
    if await filter_out_category(page):
        return False
    if await filter_out_blog(page):
        return False
    return True