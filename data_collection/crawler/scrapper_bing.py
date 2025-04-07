# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Testing   - Image Scraper (Bing Browser Engine)

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import time
import imagehash
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService

def download_images(query, num_images, download_path, delay=1.5):
    edge_driver_path = "./msedgedriver.exe"  # Path to the Edge WebDriver in the same folder
    options = webdriver.EdgeOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Edge(service=EdgeService(edge_driver_path), options=options)
    driver.get("https://www.bing.com/images/search?q=" + query + "&qft=+filterui:imagesize-large+filterui:photo-photo&form=IRFLTR")

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    image_hashes = set()
    count = 0
    
    while count < num_images:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        image_links = soup.find_all("a", {"class": "iusc"})

        for image_link in image_links:
            if count >= num_images:
                break

            try:
                m = image_link["m"]
                m = m.split(',"murl":"')[1].split('","')[0]  # Extract the original image URL
                image_url = m.replace('\\', '')
                img_response = requests.get(image_url)
                img = Image.open(BytesIO(img_response.content))

                img_hash = imagehash.average_hash(img)
                if img_hash in image_hashes:
                    print(f"Duplicate image found and skipped: {image_url}")
                    continue
                image_hashes.add(img_hash)

                image_filename = os.path.join(download_path, f"{query}_{count}.jpg")
                img.save(image_filename, "JPEG")

                print(f"Downloaded: {image_filename}")
                count += 1
            except Exception as e:
                print(f"Could not download image {count}: {e}")

        time.sleep(delay)

    driver.quit()

if __name__ == "__main__":
    query = "Leaf curl"
    num_images = 400
    download_path = "./downloaded_images"
    download_images(query, num_images, download_path)
