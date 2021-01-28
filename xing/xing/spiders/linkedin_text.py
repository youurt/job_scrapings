import scrapy
import pandas as pd
from scrapy import Request
import re


class LinkedinTextSpider(scrapy.Spider):
    name = 'linkedin_text'

    def start_requests(self):
        for index, row in pd.read_csv(f"data_{self.cat}/linkedin/linkedin_raw.csv").iterrows():
            yield Request(
                url=row["link"],
                dont_filter=True,
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "accept-encoding": "gzip, deflate, sdch, br",
                    "accept-language": "en-US,en;q=0.8,ms;q=0.6",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
                },
                callback=self.parse_text,
                cb_kwargs=dict(link=row["link"], job_id=row["job_id"]))

    def parse_text(self, response, link, job_id):

        text = self.cleanhtml(" ".join(response.css(".show-more-less-html__markup").css(
            ".show-more-less-html__markup--clamp-after-5").getall()))

        company_name = " ".join(response.css(
            ".sub-nav-cta__optional-url").css("a::attr(title)").getall())

        print(link, company_name, job_id, text)

        yield {"link": link, "text": text, "company_name": company_name, "job_id": job_id}

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = cleantext.replace("\n", "")
        cleantext = cleantext.replace("\t", "")
        cleantext = cleantext.replace("\r", "")
        return cleantext.strip()
