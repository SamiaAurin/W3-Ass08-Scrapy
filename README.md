# Trip.com Scraper Project

## Project Overview

This project is a web scraper designed to extract hotel property information from [Trip.com](https://uk.trip.com/hotels/?locale=en-GB&curr=GBP). It uses Scrapy, a powerful Python web scraping framework, to gather data on various hotel properties. The extracted data is then stored in a PostgreSQL database using SQLAlchemy. Images of the hotels are downloaded and stored locally in a directory, with the image paths stored in the database for future reference. The project aims to provide a dynamic and usable system for gathering hotel data.

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Database Configuration](#database-configuration)
- [Code Coverage](#code-coverage)
- [Known Issues](#known-issues)


## Installation

### Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.10+** (for local development)
- **Docker and Docker Compose**
   - Follow the official Docker installation guide to install Docker on your system: [Docker Installation Guide](https://docs.docker.com/desktop/)


### Steps
For a step-by-step guide on running the necessary commands and visualizing the project's database or output after cloning the repository, download the `Assignment-Scrapy.pdf` file included in the project.

1. Clone the repository

   ```bash
   git clone https://github.com/SamiaAurin/W3-Ass08-Scrapy.git
   cd W3-Ass08-Scrapy
   ```
2. Set Up a Virtual Environment

   On Linux/macOS:

    ```bash
    python3 -m venv venv  # or python -m venv venv 
    source venv/bin/activate
    ```
   On Windows:

    ```bash
    python3 -m venv venv   # or python -m venv venv 
    venv\Scripts\activate
    ```
3. Docker Desktop    
   
   Ensure Docker Desktop is running on your system, as it is required to manage the containers. Then, execute the following commands to build and run the application:

    ```bash
    cd travelscraper
    docker-compose build
    docker-compose up
    ```
    To stop the application, press `Ctrl + C` or run: 

    ```bash
    docker-compose down
    ```
    **Note:** The Docker build process may take some time to complete. This is because the `Dockerfile` and `docker-compose.yml` are configured to automatically install all dependencies listed in the `requirements.txt` file during the build phase. Please be patient while the setup is finalized.   

## Project Structure

The project follows a standard Scrapy project structure. Here’s an overview:

```bash
    travelcscraper/
    │   ├── images        #create a folder named images or it will be auto created.       
    │   ├── tests
    │   ├── travelcscraper/ 
    │   │   ├── spiders/
    │   │   │   ├── __init__.py
    │   │   │   └── hotel_info.py
    │   │   ├── _init_.py
    │   │   ├── items.py
    │   │   ├── middlewares.py
    │   │   ├── pipelines.py
    │   │   └── settings.py
    │   ├── docker-compose.yml
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── scrapy.cfg
    venv
    .gitignore
    commands.txt
    README.md    
```
- **spiders/hotel_info_spider.py:** Contains the Scrapy spider that scrapes hotel information.

- **items.py:** Defines the data structure for storing scraped data.

- **pipelines.py:** Handles processing the scraped data (e.g., storing it in the PostgreSQL database and saving images).

- **settings.py:** Configures Scrapy settings, including database connection and other spider settings.

- **Dockerfile:** Defines the Docker container for the scraper.

- **docker-compose.yml:** Configures Docker containers for both the Scrapy scraper and PostgreSQL database.


## Usage

### Storing Images
Images will be automatically downloaded and stored in a directory called `images`. The image file names will be stored as references in the database for later use.

### Storing Data in PostgreSQL
The scraper will automatically create the necessary database table and store hotel property data such as title, rating, location, latitude, longitude, room type, price, and image references.

#### Viewing Database Tables in the Docker Container
To inspect the database tables and view their data within the PostgreSQL container, follow these steps:

1. Access the PostgreSQL Container
Run the following command to open a bash shell inside the running database container:
```bash
docker exec -it travelscraper-db-1 bash
```
2. Connect to the PostgreSQL Database
```bash
psql -U username -d hotels_data
```
3. Query the Database
To view the data in the `hotels` table, execute the following SQL command:

```bash
SELECT * FROM hotels;
```
This will display all the records stored in the `hotels` table.


## Database Configuration

The connection string for PostgreSQL is stored in the environment variable `DATABASE_URL`. Here is an example of the connection string format:

```bash
postgresql://username:password@db/hotels_data
```
- **username:** The PostgreSQL username.
- **password**: The PostgreSQL password.
- **db**: The database name (this should be created beforehand or automatically, Check `docker-compose.yml`).
- **hotels_data**: The table where hotel data will be stored.

Make sure to adjust the DATABASE_URL environment variable in `docker-compose.yml` or your environment settings accordingly.    


## Code Coverage

This can be tested using:

```bash
pip install coverage requests sqlalchemy
coverage run -m unittest tests\test.py
coverage report
```

**Note:** During the test execution, you may notice a log message like the following:
```bash
Failed to download image https://invalid-url/test.jpg: HTTPSConnectionPool(host='invalid-url', port=443): Max retries exceeded with url: /test.jpg (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x000001B09914D2B0>: Failed to resolve 'invalid-url' ([Errno 11001] getaddrinfo failed)"))
```

**Why This Happens**
This message is expected and does not indicate a problem with the application. It occurs because the tests include a scenario where an invalid or dummy image URL (https://invalid-url/test.jpg) is intentionally used to verify how the application handles failures in downloading images.

**Purpose of This Test**
This test ensures that:

- The pipeline gracefully handles cases where an image URL is invalid or unreachable.
- The system does not crash and continues processing other items even when an image download fails.
- If you see this message during testing, it means the system is functioning as expected in handling invalid image URLs.

## Known Issues
If you encounter any issues related to dependencies or changes made in the `requirements.txt`, `docker-compose.yml`, or `Dockerfile`, it is recommended to rebuild the Docker containers without using the cache. This ensures that all changes are reflected and any stale layers are removed.

Run the following command to rebuild the containers:
```bash
docker-compose build --no-cache
```
This command will force Docker to rebuild the image from scratch, incorporating any updates or changes made to the configuration files.