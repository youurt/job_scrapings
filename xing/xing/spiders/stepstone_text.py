from typing import Tuple
import scrapy
import pandas as pd
from scrapy import Request
import re


class StepstoneTextSpider(scrapy.Spider):
    name = 'stepstone_text'

    def start_requests(self):
        for index, row in pd.read_csv(f"data_{self.cat}/stepstone/stepstone_raw.csv").iterrows():
            yield Request(
                url=row["link"],
                dont_filter=True,
                callback=self.parse_text,
                cb_kwargs=dict(link=row["link"], job_id=row["job_id"]))

    def parse_text(self, response, link, job_id):
        text = self.cleanhtml("".join(response.css(
            ".js-app-ld-ContentBlock").getall()).strip())
        comp_name = "".join(response.css("h1").css(
            ".at-header-company-name::text").getall())

        yield {"link": link, "text": text, "comp_name": comp_name, "job_id": job_id}

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = cleantext.replace("\n", "")
        cleantext = cleantext.replace("\t", "")
        cleantext = cleantext.replace("\r", "")
        return cleantext.strip()
