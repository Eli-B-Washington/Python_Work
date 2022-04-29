from itertools import product
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ['https://www.barnesandnoble.com/w/effective-python-brett-slatkin/1130203296?ean=9780134853987']

    def parse(self, response):
        for books in response.css('tbody'):
            try:
                yield{
                'ISBN-13': books.css('td:first-of-type::text').get(),
                'Publisher': books.css('tr:nth-child(2) > td > a > span::text').get(),
                'PublishlicationDate': books.css('tr:nth-child(3) > td::text').get(),
                'Series': books.css('tr:nth-child(4) > td > a::text').get(),
                'EditionDescription': books.css('tr:nth-child(5) > td::text').get(),
                'Pages': books.css('tr:nth-child(6) > td::text').get(),
                'SalesRank': books.css('tr:nth-child(7) > td::text').get(),
                'ProductDimensions': books.css('tr:nth-child(8) > td::text').get(),
                'Price': response.css('.d-lg-none > select > option::text ').get()
                }
            except:
                {
                print("error in Data")
            }

