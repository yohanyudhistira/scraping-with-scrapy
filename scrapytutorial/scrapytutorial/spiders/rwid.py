from typing import List

import scrapy
from cssselect import Selector


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['localhost']

    # mulai dari urls ini
    start_urls = ['http://localhost:5000/']

    def parse(self, response):
        data = {
            "username": "user",
            "password": "user12345"
        }

        return scrapy.FormRequest(
            url="http://localhost:5000/login",
            formdata=data,
            callback=self.after_login
        )

    def after_login(self, response):
        """
        2 task disini:

        1. ambil semua data produk di halaman hasil. -> akan menuju details (parsing details)
        2. ambil semua link next. -> akan kembai ke self.after_login

        :param response:
        :return:
        """

        # get product deatils
        product_details: List[Selector] = response.css(".card .card-title a")
        for details in product_details:
            href = details.attrib.get("href")
            yield response.follow(href, callback=self.parse_details)

        paginations: List[Selector] = response.css(".pagination a.page-link")
        for pagination in paginations:
            href = pagination.attrib.get("href")
            yield response.follow(href, callback=self.after_login)

    def parse_details(self, response):
        image = response.css(".card-img-top").attrib.get("src")
        title = response.css(".card-title::text").get()
        stock = response.css(".card-stock::text").get()
        description = response.css(".card-text::text").get()

        return {
            "image": image,
            "title": title,
            "stock": stock,
            "description": description
        }



