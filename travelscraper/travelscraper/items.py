import scrapy

class HotelInfoItem(scrapy.Item):
    city_id = scrapy.Field()
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    price = scrapy.Field()
    hotel_img = scrapy.Field()  # This will store the URL of the image
    rating = scrapy.Field()
    room_type = scrapy.Field()
    location = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
