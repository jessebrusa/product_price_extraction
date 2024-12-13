import asyncio
from playwright.async_api import async_playwright

async def download_html(url: str, output_file: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        await browser.close()

def save_html(url: str):
    output_file = './printout_data/downloaded_page.html'
    asyncio.run(download_html(url, output_file))

# Example usage
if __name__ == "__main__":
    url = 'https://www.guidefitter.com/armasight/shop/bnvd-40-gen-3-pinnacle-night-vision-goggle'
    save_html(url)