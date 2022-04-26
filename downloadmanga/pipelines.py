# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter


#class DownloadmangaPipeline:
  #  def process_item(self, item, spider):
    #        return item


from scrapy.pipelines.images import ImagesPipeline

class CustomMangaImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return request.url.split('/')[-1]