import os
import requests
from sqlalchemy.orm import sessionmaker
from .items import Hotel, get_engine_and_session

class HotelPipeline:

    def open_spider(self, spider):
        # Initialize database session
        database_url = os.getenv("DATABASE_URL", "postgresql://username:password@db:5432/hotels_data")
        engine, self.session = get_engine_and_session(database_url)

    def close_spider(self, spider):
        # Close database session
        self.session.close()

    def process_item(self, item, spider):
        # Download image
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)
        image_url = item.get('hotel_img')
        if image_url:
            image_path = self.download_image(image_url, images_dir)
            item['hotel_img'] = image_path

        # Save data to database
        hotel = Hotel(
            city_id=item.get("city_id"),
            hotel_id=item.get("hotel_id"),
            hotel_name=item.get("hotel_name"),
            price=item.get("price"),
            hotel_img=item.get("hotel_img"),
            rating=item.get("rating"),
            room_type=item.get("room_type"),
            location=item.get("location"),
            latitude=item.get("latitude"),
            longitude=item.get("longitude"),
        )
        self.session.add(hotel)
        self.session.commit()

        return item

    def download_image(self, url, images_dir):
        image_name = os.path.basename(url)
        image_path = os.path.join(images_dir, image_name)
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                return image_path
        except Exception as e:
            print(f"Failed to download image {url}: {e}")
        return None
