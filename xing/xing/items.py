import scrapy


class XingItem(scrapy.Item):
    title = scrapy.Field()
    company_name = scrapy.Field()
    link = scrapy.Field()
    location = scrapy.Field()
    days_diff = scrapy.Field()
    text = scrapy.Field()
    company_link = scrapy.Field()
    activatedAt = scrapy.Field()
