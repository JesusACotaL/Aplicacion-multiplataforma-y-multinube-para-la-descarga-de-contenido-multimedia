from services.manganelo_scraper import ManganeloScraper


def scraper_handler(event: dict, context: str) -> dict:
    """
    Get manga chapters GET method handler

    Args:
        event (dict): lambda event
        context (str): lambda context

    Returns:
        dict: Manga chapters response
    """
    print(event)
    print(context)

    request_body = event.get("body")
    chapter_url = request_body.get("url")
    scraper = ManganeloScraper() 
    chapters_raw = scraper.crawl_chapters(chapter_url)
    response = []
    for key, value  in chapters_raw.items():
        response.append({"Nombre": key, "Url": value})
    
    return response
