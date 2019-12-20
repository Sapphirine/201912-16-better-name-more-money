import json
import collections
import re
import numpy as np
import logging
import sys
import scrapy
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from airbnb_scrape.items import AirbnbScraperItem
from inline_requests import inline_requests

# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com']
    key = 'd306zoyjsyarp7ifhu67rjxn52tv0t20'
    client_session_id = '81160313-ce62-41de-b1af-4622241be24e'

    def __init__(self, min='', *args, **kwargs):
        super(AirbnbSpider, self).__init__(*args, **kwargs)
        self.min = int(min)

    review_url = 'https://www.airbnb.com/api/v2/homes_pdp_reviews?currency=USD' \
                 '&key={0}' \
                 '&locale=en' \
                 '&listing_id={1}' \
                 '&_format=for_p3&limit=700&offset=0&order=language_country'

    house_url = 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web' \
              '&auto_ib=false' \
              '&client_session_id={1}' \
              '&currency=USD&current_tab_id=home_tab' \
              '&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true' \
              '&items_per_grid=18' \
              '&key={0}' \
              '&locale=en' \
              '&metadata_only=false' \
              '&query=New%20York' \
              '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_version=1.1.7&screen_height=739&screen_size=medium&screen_width=900&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true' \
              '&timezone_offset=-300&version=1.6.5'

    def start_requests(self):
        self.house_url = self.house_url + '&price_min={2}&price_max={3}'
        self.max = self.min + 19
        new_url = self.house_url.format(self.key, self.client_session_id, self.min, self.max)
        yield scrapy.Request(url=new_url, callback=self.parse_id, dont_filter=False)

    @inline_requests
    def parse_id(self, response):
        # print('parsing id')
        data = json.loads(response.body)
        homes = data.get('explore_tabs')[0].get('sections')[0].get('listings')
        pagination_metadata = data.get('explore_tabs')[0].get('pagination_metadata')
        if homes is None:
            try:
                homes = data.get('explore_tabs')[0].get('sections')[1].get('listings')
            except IndexError:
                try:
                    homes = data.get('explore_tabs')[0].get('sections')[2].get('listings')
                except:
                    raise CloseSpider("No homes available in the city and price parameters")
        data_dict = collections.defaultdict(dict)
        base_url = 'https://www.airbnb.com/rooms/'
        for home in homes:
            # room_id = str(home.get('listing').get('id'))
            # url = base_url + str(home.get('listing').get('id'))
            # data_dict[room_id]['url'] = url
            # data_dict[room_id]['listing_id'] = room_id
            # data_dict[room_id]['price'] = home.get('pricing_quote').get('rate').get('amount')
            # data_dict[room_id]['bathrooms'] = home.get('listing').get('bathrooms')
            # data_dict[room_id]['bedrooms'] = home.get('listing').get('bedrooms')
            # data_dict[room_id]['host_languages'] = home.get('listing').get('host_languages')
            # data_dict[room_id]['is_business_travel_ready'] = home.get('listing').get('is_business_travel_ready')
            # data_dict[room_id]['is_fully_refundable'] = home.get('listing').get('is_fully_refundable')
            # data_dict[room_id]['is_new_listing'] = home.get('listing').get('is_new_listing')
            # data_dict[room_id]['is_superhost'] = home.get('listing').get('is_superhost')
            # data_dict[room_id]['lat'] = home.get('listing').get('lat')
            # data_dict[room_id]['lng'] = home.get('listing').get('lng')
            # data_dict[room_id]['localized_city'] = home.get('listing').get('localized_city')
            # data_dict[room_id]['localized_neighborhood'] = home.get('listing').get('localized_neighborhood')
            # data_dict[room_id]['listing_name'] = home.get('listing').get('name')
            # data_dict[room_id]['person_capacity'] = home.get('listing').get('person_capacity')
            # data_dict[room_id]['picture_count'] = home.get('listing').get('picture_count')
            # data_dict[room_id]['reviews_count'] = home.get('listing').get('reviews_count')
            # data_dict[room_id]['room_type_category'] = home.get('listing').get('room_type_category')
            # data_dict[room_id]['star_rating'] = home.get('listing').get('star_rating')
            # data_dict[room_id]['host_id'] = home.get('listing').get('user').get('id')
            # data_dict[room_id]['avg_rating'] = home.get('listing').get('avg_rating')
            # data_dict[room_id]['can_instant_book'] = home.get('pricing_quote').get('can_instant_book')
            # data_dict[room_id]['monthly_price_factor'] = home.get('pricing_quote').get('monthly_price_factor')
            # data_dict[room_id]['currency'] = home.get('pricing_quote').get('rate').get('currency')
            # data_dict[room_id]['amt_w_service'] = home.get('pricing_quote').get('rate_with_service_fee').get('amount')
            # data_dict[room_id]['rate_type'] = home.get('pricing_quote').get('rate_type')
            # data_dict[room_id]['weekly_price_factor'] = home.get('pricing_quote').get('weekly_price_factor')
            # data_dict[room_id]['min_nights'] = home.get('listing').get('min_nights')
            # data_dict[room_id]['max_nights'] = home.get('listing').get('max_nights')
            listing = AirbnbScraperItem()
            room_id = str(home.get('listing').get('id'))
            url = base_url + str(home.get('listing').get('id'))
            listing['listing_id'] = room_id
            listing['url'] = url
            listing['price'] = home.get('pricing_quote').get('rate').get('amount')
            listing['bathrooms'] = home.get('listing').get('bathrooms')
            listing['bedrooms'] = home.get('listing').get('bedrooms')
            listing['is_superhost'] = home.get('listing').get('is_superhost')
            listing['lat'] = home.get('listing').get('lat')
            listing['lng'] = home.get('listing').get('lng')
            listing['localized_city'] = home.get('listing').get('localized_city')
            listing['listing_name'] = home.get('listing').get('name')
            listing['person_capacity'] = home.get('listing').get('person_capacity')
            listing['reviews_count'] = home.get('listing').get('reviews_count')
            listing['room_type_category'] = home.get('listing').get('room_type_category')
            listing['can_instant_book'] = home.get('pricing_quote').get('can_instant_book')
            listing['min_nights'] = home.get('listing').get('min_nights')
            listing['max_nights'] = home.get('listing').get('max_nights')
            new_reiews_url = self.review_url.format(self.key, room_id)
            resp = yield scrapy.Request(url=new_reiews_url)
            data = json.loads(resp.body)
            reviews = data.get('reviews')
            last = reviews[0].get('created_at')[0:10]
            first = reviews[-1].get('created_at')[0:10]
            diff = (int(last[0:4]) - int(first[0:4])) * 12 + int(last[5:7]) - int(first[5:7])
            listing['months'] = diff
            yield listing
        # After scraping entire listings page, check if more pages
        # for room_id in data_dict:
        #     yield SplashRequest(url=base_url+room_id, callback=self.parse_details,
        #                         meta=data_dict.get(room_id),
        #                         endpoint="render.html",
        #                         args={'wait': '0.5'})

        if pagination_metadata.get('has_next_page'):
            items_offset = pagination_metadata.get('items_offset')
            section_offset = pagination_metadata.get('section_offset')
            new_url = self.house_url.format(self.key, self.client_session_id, self.min, self.max) + \
                      '&items_offset={0}&section_offset={1}'.format(items_offset, section_offset)
            print('next page')
            yield scrapy.Request(url=new_url, callback=self.parse_id)

    @inline_requests
    def parse_details(self, response):
        listing = AirbnbScraperItem()
        listing_id =  response.meta['listing_id']
        new_reiews_url = self.review_url.format(self.key, listing_id)
        listing['listing_id'] = listing_id
        listing['is_superhost'] = response.meta['is_superhost']
        listing['price'] = response.meta['price']
        listing['url'] = response.meta['url']
        listing['bathrooms'] = response.meta['bathrooms']
        listing['bedrooms'] = response.meta['bedrooms']
        listing['lat'] = response.meta['lat']
        listing['lng'] = response.meta['lng']
        listing['localized_city'] = response.meta['localized_city']
        listing['listing_name'] = response.meta['listing_name']
        listing['person_capacity'] = response.meta['person_capacity']
        listing['reviews_count'] = response.meta['reviews_count']
        listing['room_type_category'] = response.meta['room_type_category']
        listing['can_instant_book'] = response.meta['can_instant_book']
        listing['min_nights'] = response.meta['min_nights']
        listing['max_nights'] = response.meta['max_nights']
        # try:
        #     listing['num_beds'] = int((re.search('"bed_label":"(.).*","bedroom_label"', response.text)).group(1))
        # except:
        #     listing['num_beds'] = 0
        resp = yield scrapy.Request(url=new_reiews_url)
        data = json.loads(resp.body)
        reviews = data.get('reviews')
        last = reviews[0].get('created_at')[0:10]
        first = reviews[-1].get('created_at')[0:10]
        diff = (int(last[0:4]) - int(first[0:4])) * 12 + int(last[5:7]) - int(first[5:7])
        listing['months'] = diff
        yield listing
