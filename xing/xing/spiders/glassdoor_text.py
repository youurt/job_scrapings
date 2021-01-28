import scrapy
import pandas as pd
from scrapy import Request
import re


class GlassdoorTextSpider(scrapy.Spider):
    name = 'glassdoor_text'

    def start_requests(self):
        # for item in pd.read_csv(f"data_{self.topic}/glassdoor_raw.csv", converters={"link": lambda x: str(x)}):

        for index, row in pd.read_csv(f"data_{self.cat}/glassdoor/glassdoor_raw.csv").iterrows():
            yield Request(
                url=row['link'],
                dont_filter=True,
                callback=self.parse_text,
                cb_kwargs=dict(link=row['link'], job_id=row['job_id']))

    def parse_text(self, response, link, job_id):
        text = self.cleanhtml("".join(response.css(
            "#JobDescriptionContainer").css(".desc").getall()))
        yield {"text": text, "job_id": job_id, "link": link}

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = cleantext.replace("\n", "")
        cleantext = cleantext.replace("\t", "")
        cleantext = cleantext.replace("\r", "")
        return cleantext.strip()
