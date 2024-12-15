import scrapy
import json
import re
import random
from urllib.parse import urlparse

class HotelInfoSpider(scrapy.Spider):
    name = "hotel_info"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        self.log("Response received!")
        script = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                json_str = match.group(1)
                try:
                    json_data = json.loads(json_str)
                     # Randomly choose between 'inboundCities' or 'outboundCities'
                    cities = random.choice([
                        json_data.get('initData', {}).get('htlsData', {}).get('inboundCities', []),
                        json_data.get('initData', {}).get('htlsData', {}).get('outboundCities', [])
                    ])

                    if cities:
                        city = random.choice(cities)
                        city_id = city.get('id')
                        if city_id:
                            hotels_url = f"https://uk.trip.com/hotels/list?city={city_id}"
                            yield scrapy.Request(url=hotels_url, callback=self.parse_hotels)
                            
                except json.JSONDecodeError as e:
                    self.log(f"JSON decoding failed: {e}")

    def parse_hotels(self, response):
        script = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if script:
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                json_str = match.group(1)
                try:
                    json_data = json.loads(json_str)
                    hotel_list = json_data.get('initData', {}).get('firstPageList', {}).get('hotelList', [])

                    for hotel in hotel_list:
                        coordinate = hotel.get("positionInfo", {}).get("coordinate", {})
                        yield {
                            "hotel_name": hotel.get("hotelBasicInfo", {}).get("hotelName"),
                            "price": hotel.get("hotelBasicInfo", {}).get("price"),
                            "hotel_img": hotel.get("hotelBasicInfo", {}).get("hotelImg"),
                            "rating": hotel.get("commentInfo", {}).get("commentScore"),
                            "room_type": hotel.get("roomInfo", {}).get("physicalRoomName"),
                            "location": hotel.get("positionInfo", {}).get("positionName"),
                            "latitude": coordinate.get("lat"),
                            "longitude": coordinate.get("lng"),
                        }
                except json.JSONDecodeError as e:
                    self.log(f"JSON decoding failed: {e}")
