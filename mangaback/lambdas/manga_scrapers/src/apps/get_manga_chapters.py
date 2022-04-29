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
    chapters_url = request_body.get("url")

    scraper = ManganeloScraper()

    return scraper.crawl_chapters(chapters_url)
