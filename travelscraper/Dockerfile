# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Default command to run Scrapy spider
#CMD ["scrapy", "crawl", "hotel_info", "-s", "LOG_LEVEL=DEBUG"]
CMD ["scrapy", "crawl", "hotel_info"]
