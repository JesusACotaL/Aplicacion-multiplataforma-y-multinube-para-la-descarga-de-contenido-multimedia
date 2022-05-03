from typing import List
from bs4 import BeautifulSoup
from lxml import etree
from utils.request_utils import RequestUtils
from services.manga_scraper import MangaScraper


class ManganeloScraperException(Exception):
    pass


class ManganeloScraper(MangaScraper):
    def __init__(self) -> None:
        images_xpath = "//div[contains(@class, 'container-chapter-reader')]//img"
        chapters_xpath = "//div[contains(@class, 'panel-story-chapter-list')]/ul[contains(@class, 'row-content-chapter')]/li/a"
        info_xpath = "//div[contains(@class, 'panel-search-story')]//div[contains(@class, 'search-story-item')]"
        MangaScraper.__init__(
            self,
            images_xpath=images_xpath,
            chapters_xpath=chapters_xpath,
            info_xpath=info_xpath,
        )

    def crawl_info(self, search_url: str) -> List[str]:
        """
        Gets manga info from search_url

        Args:
            search_url (str): Url with search results

        Returns:
            List[str]: List of info (images, name, author, stars, etc..)
        """
        chapters_xpath = "div/h3//a"
        author_xpath = "div//span[contains(@class, 'item-author')]"
        image_xpath = "a//img"
        star_xpath = "a//em[contains(@class, 'item-rate')]"

        info: List[str] = []
        info_response = RequestUtils.call_get_request(search_url)
        info_doc = BeautifulSoup(info_response.text, "html.parser")
        info_dom = etree.HTML(str(info_doc))

        info_element = info_dom.xpath(self.info_xpath)

        for inf in info_element:

            manga_info = {
                "name": inf.xpath(chapters_xpath)[0].text,
                "author": inf.xpath(author_xpath)[0].text,
                "image_url": inf.xpath(image_xpath)[0].get("src"),
                "chapters_url": inf.xpath(chapters_xpath)[0].get("href"),
                "stars": inf.xpath(star_xpath)[0].text,
            }
            info.append(manga_info)

        return info
