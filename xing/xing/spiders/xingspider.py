import scrapy
from scrapy import Request
import requests
import json
from datetime import datetime
from scrapy.selector import Selector
from xing.items import XingItem

DAYS_FILTER = 14
FILTER = ["php", ".net", "senior", "rails", "laravel",
          "sap", "c#", "java", "ios", "backend", "drupal", "cms"]


class XingspiderSpider(scrapy.Spider):
    name = 'xingspider'

    def start_requests(self):
        # words = "Web%20Developer%20junior"
        words = self.search_params
        r = requests.get(
            f"https://www.xing.com/jobs/api/search?sc_o=jobs_search_button&sc_o_PropActionOrigin=navigation_badge_jobs_2&keywords={words}&limit=20")
        limit = r.json()["meta"]["count"]
        # limit = 20
        yield Request(
            url=f"https://www.xing.com/jobs/api/search?sc_o=jobs_search_button&sc_o_PropActionOrigin=navigation_badge_jobs_2&keywords={words}&limit={limit}",
            dont_filter=True,
            callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        for item in data["items"]:
            company_name = item["company"]["name"]
            company_link = item["company"]["link"]
            link = item["link"]
            location = item["location"]
            title = item["title"]
            activatedAt = item["activatedAt"]
            days_diff = int(self.make_diff_days(activatedAt))
            if days_diff < DAYS_FILTER:
                yield Request(
                    url=link,
                    dont_filter=True,
                    callback=self.parse_text,
                    cb_kwargs=dict(company_name=company_name,
                                   link=link, location=location, title=title, activatedAt=activatedAt, days_diff=days_diff, company_link=company_link))

            # if days_diff < 14 and not "senior" in title.lower() and not "php" in title.lower():

            # if days_diff < DAYS_FILTER:
            #     res = any(
            #         el in title.lower() for el in FILTER)
            #     if not res:
            #         yield Request(
            #             url=link,
            #             dont_filter=True,
            #             callback=self.parse_text,
            #             cb_kwargs=dict(company_name=company_name,
            #                            link=link, location=location, title=title, days_diff=days_diff, company_link=company_link))

    def parse_text(self, response, company_name, link, location, title, days_diff, activatedAt, company_link):
        text = " ".join(Selector(text=response.text).css("#content").xpath(
            "//div[contains(@class, 'html-description-withShowMoreInMobile-container')]").css("p::text").getall())
        # res = any(
        #     el in text.lower() for el in FILTER)
        # if not res:
        yield XingItem(title=title, company_name=company_name, company_link=company_link, link=link, location=location, days_diff=days_diff, text=text.replace("\n", "").strip(), activatedAt=activatedAt)
        # yield {"title": title, "company_name": company_name, "link": link, "location": location, "days_diff": days_diff, "text": text.replace("\n", "").strip()}

        # if company_link:
        #     yield Request(
        #         url=company_link,
        #         dont_filter=True,
        #         callback=self.parse_company_data,
        #         cb_kwargs=dict(title=title, company_name=company_name, company_link=company_link, link=link, location=location, days_diff=days_diff, text=text.replace("\n", "").strip()))

    # def parse_company_data(self, response, title, company_name, company_link, link, location, days_diff, text):
    #     # sel = Selector(text=response.text)
    #     adress = response.xpath(
    #         '//div[@itemprop="streetAddress"]/text()').extract_first()
    #     postal_code = response.xpath(
    #         '//span[@itemprop="postalCode"]/text()').extract_first()
    #     city = response.xpath(
    #         '//span[@itemprop="addressLocality"]/text()').extract_first()
    #     country = response.xpath(
    #         '//div[@itemprop="addressCountry"]').css("span::text").extract_first()
    #     yield CompanyItem(company_link=company_link, adress=adress, postal_code=postal_code, city=city, country=country)
    #     # yield{"company_link": company_link, "adress": adress, "postal_code": postal_code, "city": city, "country": country}

    def make_diff_days(self, activated_at):
        datetime_object = datetime.strptime(activated_at, "%Y-%m-%dT%H:%M:%SZ")
        diff = datetime.now() - datetime_object
        return diff.days
