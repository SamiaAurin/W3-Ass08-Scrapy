import scrapy
import json
import re

class CitySpider(scrapy.Spider):
    name = "city_spider"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract the script tag containing 'window.IBU_HOTEL'
        script = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if script:
            self.log(f"Script content: {script[:1000]}")  # Log the first 1000 characters of the script for inspection

            try:
                # Use regex to find the JSON data associated with window.IBU_HOTEL
                match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', script, re.DOTALL)
                if match:
                    # Extract the JSON part
                    json_data_str = match.group(1).strip()

                    # Try loading the JSON data
                    json_data = json.loads(json_data_str)

                    # Access 'initData.htlsData' directly
                    htls_data = json_data.get('initData', {}).get('htlsData', {})

                    # Extract the required arrays from htlsData
                    inbound_cities = htls_data.get('inboundCities', [])
                    outbound_cities = htls_data.get('outboundCities', [])
                    five_star_hotels = htls_data.get('fiveStarHotels', [])
                    cheap_hotels = htls_data.get('cheapHotels', [])
                    hostel_hotels = htls_data.get('hostelHotels', [])

                    # Combine the data in a dictionary
                    data = {
                        'inbound_cities': inbound_cities,
                        'outbound_cities': outbound_cities,
                        'five_star_hotels': five_star_hotels,
                        'cheap_hotels': cheap_hotels,
                        'hostel_hotels': hostel_hotels
                    }

                    # Save data to a JSON file
                    with open('output.json', 'w') as json_file:
                        json.dump(data, json_file, indent=4)

                    # Optionally, yield the data if needed
                    yield data
                else:
                    self.log("Could not find 'window.IBU_HOTEL' using regex")
            except (IndexError, json.JSONDecodeError, re.error) as e:
                self.log(f"Error extracting JSON data: {e}")
        else:
            self.log("Could not find the script containing IBU_HOTEL")
