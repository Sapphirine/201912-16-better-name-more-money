# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def remove_unicode(value):
    return value.replace(u"\u201c", '').replace(u"\u201d", '').replace(u"\2764", '').replace(u"\ufe0f")

class AirbnbScraperItem(scrapy.Item):
    # Host Fields
    is_superhost = scrapy.Field()
    listing_id = scrapy.Field()
    # Room Fields
    price = scrapy.Field()
    url = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    localized_city = scrapy.Field()
    listing_name = scrapy.Field(input_processor=MapCompose(remove_unicode))
    person_capacity = scrapy.Field()
    reviews_count = scrapy.Field()
    room_type_category = scrapy.Field()
    can_instant_book = scrapy.Field()
    bathrooms = scrapy.Field()
    bedrooms = scrapy.Field()
    months= scrapy.Field()
    min_nights = scrapy.Field()
    max_nights = scrapy.Field()
