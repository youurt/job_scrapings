import scrapy
from scrapy.http.request import Request
from scrapy.selector import Selector
import logging
logger = logging.getLogger(__name__)


KEYWORDS = "junior+web+developer"
NO_GOES = "+-java+-php+-senior+-.net+-c%23"


class IndeedSpider(scrapy.Spider):
    name = 'indeed'

    def start_requests(self):
        yield Request(
            url=f"https://de.indeed.com/Jobs?q={KEYWORDS}{NO_GOES}&l=Deutschland&radius=25&start",
            dont_filter=True,
            callback=self.parse_pages)

    def parse_pages(self, response):
        elements = response.css(
            ".jobsearch-SerpJobCard").getall()

        for element in elements:
            html = Selector(text=element)
            title = html.css("h2").css(
                ".title").css("a::attr(title)").getall()
            link = "https://de.indeed.com/Zeige-Job"+"".join(html.css("h2").css(
                ".title").css("a::attr(href)").getall())[7:]
            company = html.css(
                ".sjcl").css(".company::text").getall()
            if "\n" in company:
                company = html.css(".sjcl").css(
                    ".company").css("a::text").getall()
            company = "".join(company).replace("\n", "")
            location = "".join(html.css(
                ".sjcl").css(".location::text").getall())
            activated = "".join(html.css(
                ".result-link-bar").css(".date::text").getall())
            yield {"title": title, "link": link, "company": company, "location": location, "activated": activated}

        print(response)
        if 'span class="np"' in response.css(
                ".pagination-list").css("li").getall()[-1]:
            yield Request(
                url="https://de.indeed.com"+response.css(
                    ".pagination-list").css("li").css("a::attr(href)").getall()[-1],
                dont_filter=True,
                callback=self.parse_pages)
