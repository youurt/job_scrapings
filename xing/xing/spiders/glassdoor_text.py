import scrapy
import pandas as pd
from scrapy import Request
import re


class GlassdoorTextSpider(scrapy.Spider):
    name = 'glassdoor_text'

    def start_requests(self):
        for link in pd.read_csv("res_glassdoor.csv", converters={"link": lambda x: str(x)})["link"]:
            yield Request(
                url=link,
                dont_filter=True,
                callback=self.parse_text,
                cb_kwargs=dict(link=link))

    def parse_text(self, response, link):
        text = self.cleanhtml("".join(response.css(
            "#JobDescriptionContainer").css(".desc").getall()))
        yield {"text": text, "link": link}

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = cleantext.replace("\n", "")
        cleantext = cleantext.replace("\t", "")
        cleantext = cleantext.replace("\r", "")
        return cleantext.strip()
