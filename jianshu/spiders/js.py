import scrapy
from ..items import JianshuItem

class JsSpider(scrapy.Spider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/c/22f2ca261b85?page=1']

    def parse(self, response):
        li_list = response.xpath("//ul[@class='note-list']/li")
        for li in li_list:
            item = JianshuItem()
            item['title'] = li.xpath(".//a[@class='title']/text()").extract_first()
            item['img'] = li.xpath("./a[@class='wrap-img']/img/@src").extract_first()
            item['abstract'] = li.xpath(".//p[@class='abstract']/text()").extract_first().strip()
            item['author'] = li.xpath(".//a[@class='nickname']/text()").extract_first()
            item['comment'] = li.xpath(".//div[@class='meta']/a[2]/text()").extract()
            item['comment'] = [i.strip() for i in item['comment'] if len(i.strip()) > 0]
            item['like'] = li.xpath(".//div[@class='meta']/span[2]/text()").extract()
            item['like'] = [i.strip() for i in item['like'] if len(i.strip()) > 0]
            yield item
