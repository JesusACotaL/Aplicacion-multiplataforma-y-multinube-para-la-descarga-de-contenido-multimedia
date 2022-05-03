from services.manganelo_scraper import ManganeloScraper


def scraper_handler(event: dict, context: str) -> dict:
    """
    Get manga info GET method handler

    Args:
        event (dict): lambda event
        context (context): lambda context

    Returns:
        dict: Manga info response
    """
    print(event)
    print(context)

    request_body = event.get("body")
    search_url = request_body.get("url")

    scraper = ManganeloScraper()

    return scraper.crawl_info(search_url)
