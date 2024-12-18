import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'

    def start_requests(self):
        url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = {}
        product = response.css("div.product_main")
        item["title"] = product.css("h1 ::text").extract_first()
        item['category'] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        ).extract_first()
        item['description'] = response.xpath(
            "//div[@id='product_description']/following-sibling::p/text()"
        ).extract_first()
        item['price'] = response.css('p.price_color ::text').extract_first()
        yield item
