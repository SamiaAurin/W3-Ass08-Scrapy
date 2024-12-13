import scrapy
import json
import re
import random

class HotelInfoSpider(scrapy.Spider):
    name = "hotelinfo_spider"
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

                    # Randomly choose between 'inboundCities' or 'outboundCities'
                    cities_list = random.choice([
                        json_data.get('initData', {}).get('htlsData', {}).get('inboundCities', []),
                        json_data.get('initData', {}).get('htlsData', {}).get('outboundCities', [])
                    ])

                    # Randomly choose a city from the selected list
                    if cities_list:
                        city_info = random.choice(cities_list)
                        city_name = city_info.get('name')
                        self.log(f"Chosen city: {city_name}")

                        # Save the chosen city info to a JSON file
                        with open('random_city.json', 'w') as json_file:
                            json.dump(city_info, json_file, indent=4)

                        # Construct the URL to scrape hotel data
                        city_id = city_info.get('id')
                        if city_id:
                            city_url = f"https://uk.trip.com//hotels/list?city={city_id}"
                            self.log(f"Following URL: {city_url}")

                            # Make a new request to scrape hotel data
                            yield scrapy.Request(
                                url=city_url,
                                callback=self.parse_hotels,
                                meta={'city_info': city_info}  # Pass city info to the next method
                            )
                    else:
                        self.log("No cities found in inboundCities or outboundCities")
                
                except json.JSONDecodeError as e:
                    self.log(f"Error decoding JSON: {e}")
            else:
                self.log("Could not find window.IBU_HOTEL in the script")
        else:
            self.log("Script containing window.IBU_HOTEL not found")

    def parse_hotels(self, response):
        # Get the city info from the meta data passed from the previous request
        city_info = response.meta.get('city_info')
        city_id = city_info.get('id') if city_info else None

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

                    # Extract desired fields for each hotel
                    filtered_hotels = []
                    for hotel in hotel_list:
                        coordinate = hotel.get("positionInfo", {}).get("coordinate", {})
                        filtered_data = {
                            "city_id": city_id,  # Save city_id here
                            "hotelBasicInfo": {
                                "hotelId": hotel.get("hotelBasicInfo", {}).get("hotelId"),
                                "hotelName": hotel.get("hotelBasicInfo", {}).get("hotelName"),
                                "price": hotel.get("hotelBasicInfo", {}).get("price"),
                                "hotelImg": hotel.get("hotelBasicInfo", {}).get("hotelImg"),
                            },
                            "commentInfo": {
                                "commentScore": hotel.get("commentInfo", {}).get("commentScore"),
                            },
                            "roomInfo": {
                                "physicalRoomName": hotel.get("roomInfo", {}).get("physicalRoomName"),
                            },
                            "positionInfo": {
                                "positionName": hotel.get("positionInfo", {}).get("positionName"),
                                "coordinate": {
                                    "lat": coordinate.get("lat"),
                                    "lng": coordinate.get("lng"),
                                },
                            },
                        }
                        filtered_hotels.append(filtered_data)

                    # Save the extracted data to a JSON file
                    with open('random_hotels_filtered.json', 'w') as json_file:
                        json.dump(filtered_hotels, json_file, indent=4)
                    
                    self.log(f"Saved filtered hotel data to random_hotels_filtered.json")
                
                except json.JSONDecodeError as e:
                    self.log(f"Error decoding JSON: {e}")
            else:
                self.log("Could not find window.IBU_HOTEL in the script")
        else:
            self.log("Script containing window.IBU_HOTEL not found")
