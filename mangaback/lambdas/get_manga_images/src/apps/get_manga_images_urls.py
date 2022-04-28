from services.manganelo_scraper import ManganeloScraper

def lamdba_handler(event, context):
    request_body = event.get("body")
    chapter_url = request_body.get("url")
    scraper = ManganeloScraper() 

    return scraper.crawl_images(chapter_url)