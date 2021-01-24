import scrapy
import pandas as pd
from scrapy import Request


class IndeedTextSpider(scrapy.Spider):
    name = 'indeed_text'

    def start_requests(self):
        for link in pd.read_csv("res_indeed.csv", converters={"link": lambda x: str(x)})["link"]:
            yield Request(
                url=link,
                dont_filter=True,
                callback=self.parse_text,
                cb_kwargs=dict(link=link))

    def parse_text(self, response, link):
        adress = response.css(".jobsearch-JobInfoHeader-subtitle").css(
            ".jobsearch-DesktopStickyContainer-subtitle > *:last-child::text").extract_first()
        text = "".join(response.css(
            "#jobDescriptionText *::text").extract()).replace("\n", "").strip()

        yield {"adress": adress, "text": text, "link": link, }
