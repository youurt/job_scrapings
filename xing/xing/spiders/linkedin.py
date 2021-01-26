import logging
import scrapy
from scrapy import Request
from scrapy.selector import Selector

# KEYWORDS = "junior%20web%20developer"

logger = logging.getLogger(__name__)


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    start_ = 0

    def start_requests(self):
        yield Request(
            url=f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?f_E=2&f_TPR=r604800&geoId=101282230&keywords={self.search_params}&location=Deutschland",
            dont_filter=True,
            callback=self.parse_first_page)

    def parse_first_page(self, response):
        elements = response.css(
            ".result-card").css(".job-result-card").css(".result-card--with-hover-state").getall()
        for element in elements:
            link = " ".join(Selector(text=element).css(
                ".result-card__full-card-link").css("a::attr(href)").getall())
            job_name = " ".join(Selector(text=element).css(
                ".result-card__title").css(".job-result-card__title::text").getall())
            location = " ".join(Selector(text=element).css(
                ".job-result-card__location::text").getall())
            list_date = " ".join(Selector(text=element).css(
                ".job-result-card__listdate::text").getall())
            yield {"job_title": job_name, "link": link, "location": location, "activated_at": list_date}
        print(response, response.status)
        if response.status == 200:
            self.start_ += 25
            yield Request(
                url=f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?f_E=2&f_TPR=r604800&geoId=101282230&keywords={self.search_params}&location=Deutschland&start={self.start_}",
                dont_filter=True,
                callback=self.parse_first_page)
