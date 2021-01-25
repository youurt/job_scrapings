import scrapy
from scrapy import Request
from scrapy.selector import Selector

KEYWORDS = "junior-frontend-developer"


class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'
    start_ = 1

    def start_requests(self):
        yield Request(
            url=f"https://www.glassdoor.com/Job/germany-{KEYWORDS}-jobs-SRCH_IL.0,7_IN96_KO8,33.htm?fromAge=20",
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

                yield {"comp_name": comp_name, "position": position, "location": location, "link": link}
        print(response)
        disabled = response.css(".pagingControls").css(
            ".cell").css(".middle").css("li").css(".next").css("a").css("span").css(".disabled").get()
        if disabled is None:
            self.start_ += 1
            yield Request(
                url=f"https://www.glassdoor.com/Job/germany-{KEYWORDS}-jobs-SRCH_IL.0,7_IN96_KO8,33_IP{self.start_}.htm?fromAge=20",
                dont_filter=True,
                callback=self.parse_first)
