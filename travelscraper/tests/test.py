import os
from unittest import TestCase
from travelscraper.pipelines import HotelPipeline
from travelscraper.items import Hotel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from unittest.mock import patch
import requests


class TestHotelPipeline(TestCase):

    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.database_url = "sqlite:///:memory:"
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Initialize pipeline and mock database session
        self.pipeline = HotelPipeline()
        self.pipeline.session = self.session

        # Create tables
        Hotel.metadata.create_all(self.engine)

    def tearDown(self):
        # Close the database session
        self.session.close()
        self.engine.dispose()

    # Mocking the requests.get method
    @patch("requests.get")
    def test_download_image(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"fake_image_data"

        image_url = "https://example.com/fake_image.jpg"
        images_dir = "test_images"
        os.makedirs(images_dir, exist_ok=True)  # Ensure the directory exists for the test
        image_path = self.pipeline.download_image(image_url, images_dir)

        # Assert that the image was saved
        self.assertTrue(os.path.exists(image_path))
        self.assertTrue(image_path.endswith("fake_image.jpg"))

        # Clean up the created test image
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(images_dir):
            os.rmdir(images_dir)

    def test_image_download_failure(self):
        images_dir = "test_images"
        image_url = "https://invalid-url/test.jpg"
        image_path = self.pipeline.download_image(image_url, images_dir)
        self.assertIsNone(image_path)

    def test_process_item(self):
        # Mock Scrapy item
        item = {
            "city_id": 1,
            "hotel_id": 123,
            "hotel_name": "Test Hotel",
            "price": "100",
            "rating": "4.5",
            "room_type": "Deluxe",
            "location": "Test City",
            "latitude": "0.0",
            "longitude": "0.0",
            "hotel_img": "https://via.placeholder.com/150",
        }
        processed_item = self.pipeline.process_item(item, spider=None)
        self.assertIsNotNone(processed_item)
