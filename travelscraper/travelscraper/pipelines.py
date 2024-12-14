import os
import requests
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup (SQLAlchemy)
Base = declarative_base()

# Define the hotel data table in the database
class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    hotel_id = Column(Integer)
    hotel_name = Column(String)
    price = Column(Float)
    hotel_img = Column(String)  # This will store the image path
    rating = Column(Float)
    room_type = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

# Create a database engine
DATABASE_URL = "postgresql://username:password@travelscraper-db-1:5432/hotels_data"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Create the table if it doesn't exist
Session = sessionmaker(bind=engine)
session = Session()  # Creates a session to interact with the database

class HotelInfoPipeline:

    def process_item(self, item, spider):
        # Extract hotel data from item
        city_id = item['city_id']
        hotel_id = item['hotel_id']
        hotel_name = item['hotel_name']
        price = item['price']
        hotel_img = item['hotel_img']
        rating = item['rating']
        room_type = item['room_type']
        location = item['location']
        latitude = item['latitude']
        longitude = item['longitude']
        
        # Download image and save it locally
        image_path = self.download_image(hotel_img)

        # Save product data to the database
        self.save_to_database(city_id, hotel_id, hotel_name, price, image_path, rating, room_type, location, latitude, longitude)

        return item

    def download_image(self, image_url):
        # Create an "images" directory if it doesn't exist
        image_dir = "images"
        os.makedirs(image_dir, exist_ok=True)

        # Extract image name from URL
        image_name = os.path.basename(image_url)
        image_path = os.path.join(image_dir, image_name)

        # Download and save the image
        if not os.path.exists(image_path):
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(response.content)
            else:
                raise DropItem(f"Failed to download image from {image_url}")

        return image_path

    def save_to_database(self, city_id, hotel_id, hotel_name, price, hotel_img, rating, room_type, location, latitude, longitude):
        # Create a Hotel object and save it to the database
        hotel = Hotel(
            city_id=city_id,
            hotel_id=hotel_id,
            hotel_name=hotel_name,
            price=price,
            hotel_img=hotel_img,
            rating=rating,
            room_type=room_type,
            location=location,
            latitude=latitude,
            longitude=longitude
        )
        
        try:
            session.add(hotel)
            session.commit()  # Commit the transaction
        except Exception as e:
            session.rollback()  # Rollback the transaction in case of an error
            raise DropItem(f"Failed to save item {hotel_name} to database: {e}")
