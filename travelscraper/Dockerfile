# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Run the Scrapy spider named "hotelinfo_spider"
CMD ["scrapy", "crawl", "hotelinfo_spider"]