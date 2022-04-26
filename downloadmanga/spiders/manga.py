import scrapy
from downloadmanga.items import DownloadmangaItem as ImageItem

class MangaSpider(scrapy.Spider):
    name = 'manga'
    start_urls = ['https://es.wikipedia.org/wiki/México']
    #start_urls = ['https://leermanga.net/capitulo/one-piece-988.00']
    headers = {
        'manganelo': 'https://chap.manganelo.com/'
    }

    def parse(self, response):
        item = ImageItem()
        if response.status == 200:
            rel_img_urls = response.xpath("//img/@src").extract()
            item['image_urls'] = self.url_join(rel_img_urls, response)
        return item

    def url_join(self, rel_img_urls, response):
        joined_urls = []
        for rel_img_url in rel_img_urls:
            joined_urls.append(response.urljoin(rel_img_url))

        return joined_urls 
            
            
