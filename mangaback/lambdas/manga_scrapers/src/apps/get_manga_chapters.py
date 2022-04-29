from services.manganelo_scraper import ManganeloScraper

def scraper_handler(event, context):
    request_body = event.get("body")
    chapters_url = request_body.get("url")

    scraper = ManganeloScraper() 
    
    return scraper.crawl_chapters(chapters_url)