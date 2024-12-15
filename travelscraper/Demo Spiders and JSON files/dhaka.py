import scrapy
import json
import re

class DhakaSpider(scrapy.Spider):
    name = "dhaka_spider"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Call parse_city to handle the response
        return self.parse_city(response)

    def parse_city(self, response):
        # Extract the script tag containing 'window.IBU_HOTEL'
        script = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if script:
            self.log(f"Script content: {script[:1000]}")  # Log first 1000 characters of the script for inspection

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
                        self.log(f"Found Dhaka: {dhaka_info}")

                        # Save the data to a JSON file
                        with open('dhaka.json', 'w') as json_file:
                            json.dump(dhaka_info, json_file, indent=4)

                    else:
                        self.log("Dhaka not found in inboundCities")
                
                except json.JSONDecodeError as e:
                    self.log(f"Error decoding JSON: {e}")
            else:
                self.log("Could not find window.IBU_HOTEL in the script")
        else:
            self.log("Script containing window.IBU_HOTEL not found")
