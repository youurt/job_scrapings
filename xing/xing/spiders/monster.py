import scrapy
from scrapy import Request
import json
import chompjs
KEYWORDS = "junior-developer-web"


class MonsterSpider(scrapy.Spider):
    name = 'monster'

    def start_requests(self):
        for i in range(5):
            yield Request(
                url=f"https://www.monster.de/jobs/suche/pagination/?q={KEYWORDS}&cy=DE&isDynamicPage=true&isMKPagination=true&page={i}",
                dont_filter=True,
                callback=self.parse_data)

    def parse_data(self, response):
        data = json.loads(response.body)
        for item in data:
            if "Title" in item:
                company_link = ""
                title = item["Title"]
                title_link = item["TitleLink"]
                date_posted = item["DatePostedText"]
                location = item["LocationText"].strip()
                company = item["Company"]["Name"]
                if "CompanyLink" in item["Company"]:
                    company_link = item["Company"]["CompanyLink"]
                else:
                    company_link = None
                yield Request(
                    url=title_link,
                    callback=self.parse_text,
                    dont_filter=True,
                    cb_kwargs=dict(company_link=company_link, title=title, title_link=title_link,
                                   date_posted=date_posted, location=location, company=company)

    def parse_text(self, response, company_link, title, title_link, date_posted, location, company,):
        description=chompjs.parse_js_object(response.xpath(
            "//script[contains(., 'JobPosting')]/text()").extract()[0])["description"]
        yield {"company_link": company_link, "title": title, "title_link": title_link, "date_posted": date_posted, "location": location, "company": company, "description": description}
