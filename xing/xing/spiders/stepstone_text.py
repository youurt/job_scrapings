from typing import Tuple
import scrapy
import pandas as pd
from scrapy import Request
import re


class StepstoneTextSpider(scrapy.Spider):
    name = 'stepstone_text'

    def start_requests(self):
        for link in pd.read_csv("res_stepstone.csv", converters={"link": lambda x: str(x)})["link"]:
            yield Request(
                url=link,
                dont_filter=True,
                callback=self.parse_text,
                cb_kwargs=dict(link=link))

    def parse_text(self, response, link):
        text = self.cleanhtml("".join(response.css(
            ".js-app-ld-ContentBlock").getall()).strip())
        comp_name = "".join(response.css("h1").css(
            ".at-header-company-name::text").getall())

        yield {"link": link, "text": text, "comp_name": comp_name}

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = cleantext.replace("\n", "")
        cleantext = cleantext.replace("\t", "")
        cleantext = cleantext.replace("\r", "")
        return cleantext.strip()
