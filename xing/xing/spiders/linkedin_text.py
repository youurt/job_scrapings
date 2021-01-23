import scrapy
import pandas as pd
from scrapy import Request


class LinkedinTextSpider(scrapy.Spider):
    name = 'linkedin_text'

    def start_requests(self):
        for link in pd.read_csv("res.csv", converters={"link": lambda x: str(x)})["link"]:
            yield Request(
                url=link,
                dont_filter=True,
                callback=self.parse_text,
                cb_kwargs=dict(link=link))

    def parse_text(self, response, link):
        text = " ".join(response.css(".show-more-less-html__markup").css(
            ".show-more-less-html__markup--clamp-after-5").getall())
        company_name = " ".join(response.css(
            ".sub-nav-cta__optional-url").css("a::attr(title)").getall())
        company_url = self.clean_company_name(" ".join(response.css(
            ".sub-nav-cta__optional-url").css("a::attr(href)").getall()))

        yield {"link": link, "text": text, "company_name": company_name, "company_url": company_url}

    def clean_company_name(self, comp_name):
        comp_n = comp_name.split("/")[4].split("?")[0].replace(".", "")
        return f"https://www.linkedin.com/mwlite/company/{comp_n}"
