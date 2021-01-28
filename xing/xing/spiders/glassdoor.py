import scrapy
from scrapy import Request
from scrapy.selector import Selector
import uuid

# web_junior = "junior-frontend-developer"
# analyst_junior = "data-analyst-junior"
# wirtschaftsinformatiker = "wirtschaftsinformatiker"


class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'
    start_ = 1

    def start_requests(self):
        yield Request(
            url=f"https://www.glassdoor.de/Job/{self.search_params}-jobs-SRCH_KE0,19.htm?fromAge=30",
            dont_filter=True,
            callback=self.parse_first)

    def parse_first(self, response):
        items = response.css(".jlGrid").css("li").getall()
        for item in items:
            html = Selector(text=item)
            if len(item) > 1000 and len(item) < 7000:
                link = "https://www.glassdoor.com" + \
                    html.css(".jobLink").css("a::attr(href)").getall()[0]
                comp_name = html.css(".jobLink").css(
                    "a").css("span::text").getall()[0]
                position = html.css(".jobLink").css(
                    "a").css("span::text").getall()[1]
                location = "".join(html.css(".loc::text").getall())

                yield {"company_name": comp_name, "job_title": position, "location": location, "job_id": uuid.uuid4(), "link": link, }
        disabled = response.css(".pagingControls").css(
            ".cell").css(".middle").css("li").css(".next").css("a").css("span").css(".disabled").get()
        if disabled is None:
            self.start_ += 1
            yield Request(
                url=f"https://www.glassdoor.de/Job/{self.search_params}-jobs-SRCH_KO0,19_IP{self.start_}.htm?fromAge=30",
                dont_filter=True,
                callback=self.parse_first)
