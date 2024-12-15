import scrapy
import json
import re
import os
import random
import logging
from urllib.parse import urlparse
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline

class DemoSpider(scrapy.Spider):
    name = "demo"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        self.log("Response received!")
        return self.parse_city(response)

    def parse_city(self, response):
        # Extract the script tag containing 'window.IBU_HOTEL'
        logging.info("Starting crawl...")
        script = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        # Log the script length to check if we received the script correctly
        self.log(f"Script length: {len(script)}" if script else "Script not found")

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
        city_info = response.meta.get('city_info', {})
        city_name = city_info.get('name', 'unknown_city').replace(" ", "_")

        # Create a directory for storing images
        images_dir = f"images/{city_name}"
        os.makedirs(images_dir, exist_ok=True)

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
                        image_url = hotel.get("hotelBasicInfo", {}).get("hotelImg")
                        
                        # Save image to the directory
                        if image_url:
                            self.download_image(image_url, images_dir)

                        filtered_data = {
                            "hotelName": hotel.get("hotelBasicInfo", {}).get("hotelName"),
                            "price": hotel.get("hotelBasicInfo", {}).get("price"),
                            "hotelImg": image_url,
                            "rating": hotel.get("commentInfo", {}).get("commentScore"),
                            "room-type": hotel.get("roomInfo", {}).get("physicalRoomName"),
                            "location": hotel.get("positionInfo", {}).get("positionName"),
                            "latitude": coordinate.get("lat"),
                            "longitude": coordinate.get("lng"),
                        }
                        filtered_hotels.append(filtered_data)

                    # Save the extracted data to a JSON file
                    hotels_json_path = os.path.join(images_dir, 'hotels_filtered.json')
                    with open(hotels_json_path, 'w') as json_file:
                        json.dump(filtered_hotels, json_file, indent=4)
                    
                    self.log(f"Saved filtered hotel data to {hotels_json_path}")

                except json.JSONDecodeError as e:
                    self.log(f"Error decoding JSON: {e}")
            else:
                self.log("Could not find window.IBU_HOTEL in the script")
        else:
            self.log("Script containing window.IBU_HOTEL not found")

    def download_image(self, url, images_dir):
        """Download an image from the given URL and save it to the specified directory."""
        parsed_url = urlparse(url)
        image_name = os.path.basename(parsed_url.path)
        image_path = os.path.join(images_dir, image_name)

        try:
            response = scrapy.Request(url)
            with open(image_path, 'wb') as f:
                f.write(response.body)
            self.log(f"Saved image to {image_path}")
        except Exception as e:
            self.log(f"Failed to download image {url}: {e}")
