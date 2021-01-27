import scrapy
import pandas as pd
from scrapy import Request


class IndeedTextSpider(scrapy.Spider):
    name = 'indeed_text'

    def start_requests(self):
        for index, row in pd.read_csv(f"data_web_junior/indeed/indeed_raw.csv").iterrows():
            yield Request(
                url=row["link"],
                dont_filter=True,
                callback=self.parse_text,
                cb_kwargs=dict(link=row["link"], job_id=row["job_id"]))

    def parse_text(self, response, link, job_id):
        adress = response.css(".jobsearch-JobInfoHeader-subtitle").css(
            ".jobsearch-DesktopStickyContainer-subtitle > *:last-child::text").extract_first()
        text = "".join(response.css(
            "#jobDescriptionText *::text").extract()).replace("\n", "").strip()

        yield {"adress": adress, "text": text, "job_id": job_id, "link": link}
