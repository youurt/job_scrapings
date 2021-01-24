import scrapy
from scrapy import Request
from scrapy.selector import Selector
import re
KEYWORDS = "junior%20frontend%20web%20developer"


class StepstoneSpider(scrapy.Spider):
    name = 'stepstone'

    def start_requests(self):
        yield Request(
            url=f"https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&companyid=0&sourceofthesearchfield=resultlistpage%3Ageneral&qs=%5B%5D&cityid=0&ke={KEYWORDS}&radius=30&suid=713ac238-0c15-4b82-b64b-86fa623b4cef&ex=90001&ob=date&action=sort_publish",
            dont_filter=True,
            callback=self.parse_page)

    def parse_page(self, response):
        items = response.xpath(
            '//*[contains(@id, "app-dynamicResultlist")]/div/div[1]/div/div[2]/div[2]').xpath(
            '//*[contains(@id,"job-item")]/div[3]').getall()
        for item in items:
            html = Selector(text=item)
            link = "https://www.stepstone.de/" + \
                "".join(html.css("a::attr(href)").getall()).split("/")[1]
            title = "".join(html.css("h2::text").getall())

            yield {"title": title, "link": link}

        next = response.xpath(
            '//*[contains(@class,"PaginationWrapper-sc-1x0i53i-0")]').css("a::attr(href)").getall()[-1]
        print(response)
        if "paging_next" in next:
            yield Request(
                url=next,
                dont_filter=True,
                callback=self.parse_page)
