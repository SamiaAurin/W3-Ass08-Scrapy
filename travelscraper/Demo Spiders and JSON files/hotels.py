import scrapy
import json
import re

class HotelSpider(scrapy.Spider):
    name = "hotel_spider"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        return self.parse_city(response)

    def parse_city(self, response):
        # Extract the script tag containing 'window.IBU_HOTEL'
        script = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if script:
            # Use regex to extract the part containing 'window.IBU_HOTEL'
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                json_str = match.group(1)
                try:
                    # Load the JSON data
                    json_data = json.loads(json_str)

                    # Extract 'inboundCities' from the JSON data
                    inbound_cities = json_data.get('initData', {}).get('htlsData', {}).get('inboundCities', [])

                    # Look for 'Dhaka' in the inboundCities list
                    dhaka_info = next((city for city in inbound_cities if city['name'] == 'Dhaka'), None)

                    if dhaka_info:
                        # Save Dhaka city info to a JSON file
                        with open('dhaka.json', 'w') as json_file:
                            json.dump(dhaka_info, json_file, indent=4)

                        # Construct the URL to scrape hotel data
                        city_id = dhaka_info.get('id')
                        if city_id:
                            city_url = f"https://uk.trip.com//hotels/list?city={city_id}"
                            self.log(f"Following URL: {city_url}")

                            # Make a new request to scrape hotel data
                            yield scrapy.Request(
                                url=city_url,
                                callback=self.parse_dhaka_hotels,
                                meta={'city_info': dhaka_info}  # Pass city info to the next method
                            )
                    else:
                        self.log("Dhaka not found in inboundCities")
                
                except json.JSONDecodeError as e:
                    self.log(f"Error decoding JSON: {e}")
            else:
                self.log("Could not find window.IBU_HOTEL in the script")
        else:
            self.log("Script containing window.IBU_HOTEL not found")

    def parse_dhaka_hotels(self, response):
        # Extract the script tag containing 'window.IBU_HOTEL'
        script = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if script:
            # Use regex to extract the JSON object
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                json_str = match.group(1)
                try:
                    # Parse JSON data
                    json_data = json.loads(json_str)

                    # Extract hotel list from 'firstPageList.hotelList'
                    hotel_list = json_data.get('initData', {}).get('firstPageList', {}).get('hotelList', [])

                    if hotel_list:
                        # Save the hotel list to a JSON file
                        with open('dhaka_hotels.json', 'w') as json_file:
                            json.dump(hotel_list, json_file, indent=4)

                        self.log("Saved Dhaka hotels data to dhaka_hotels.json")
                    else:
                        self.log("Hotel list not found in JSON data")
                
                except json.JSONDecodeError as e:
                    self.log(f"Error decoding JSON: {e}")
            else:
                self.log("Could not find 'window.IBU_HOTEL' in the script")
        else:
            self.log("Script containing 'window.IBU_HOTEL' not found")
