from apps.get_manga_info import scraper_handler

test_body = {"body": {"url": "https://m.manganelo.com/search/story/one_piece"}}

print(scraper_handler(test_body, ""))
