# Trip.com Scraper Project

## Project Overview

This project is a web scraper designed to extract hotel property information from [Trip.com](https://uk.trip.com/hotels/?locale=en-GB&curr=GBP). It uses Scrapy, a powerful Python web scraping framework, to gather data on various hotel properties. The extracted data is then stored in a PostgreSQL database using SQLAlchemy. Images of the hotels are downloaded and stored locally in a directory, with the image paths stored in the database for future reference. The project aims to provide a dynamic and usable system for gathering hotel data.

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Database Configuration](#database-configuration)
- [Code Coverage](#code-coverage)


## Installation

### Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.10+** (for local development)
- **Docker and Docker Compose**
   - Follow the official Docker installation guide to install Docker on your system: [Docker Installation Guide](https://docs.docker.com/desktop/)
- **PostgreSQL** (if not using Docker for the database)

### Steps

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
    python -m venv venv   # or python -m venv venv 
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
    │   ├── images        #create a folder named images        
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
pip install coverage
coverage run -m unittest tests\test.py
coverage report
```