# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Testing   - Image Scraper (iNaturalist)

import os
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

target_folder = "E:\FYP\code\crawler\Asparagus_Setaceus"
taxon_id = "75604"
cur_page = 1
max_page = 100

file_name = "asparagus_setaceus"
count = 0

scroll_pause_time = 3


while(cur_page <= max_page and count <= 1000):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    edge_driver_path = "E:\FYP\code\crawler\msedgedriver.exe"

    service = Service(edge_driver_path)
    option = webdriver.EdgeOptions()
    option.add_argument(f'user-agent={user_agent}')
    option.add_experimental_option("detach", False)

    driver = webdriver.Edge(service=service, options=option)
    
    target_link = f'https://www.inaturalist.org/observations?taxon_id={taxon_id}&verifiable=any&page={cur_page}'
    driver.get(target_link)

    #Scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_data = driver.page_source

    soup = BeautifulSoup(html_data, "html.parser")
    datas = soup.find_all('a', class_="photo has-photo")

    for data in datas:
        try:
            style_attr = data.get('style', '')

            url_match = re.search(r'url\(["\']?(https?://[^"\')]+)["\']?\)', style_attr)

            if url_match:
                image_url = url_match.group(1)
                image_url = image_url.replace("medium", "large")
                resp = requests.get(image_url)
                if resp.status_code == 200:
                    with open(os.path.join(target_folder, f"{file_name}_{count}.jpg"), "wb") as file:
                        file.write(resp.content)
                        count += 1
                        time.sleep(1)
                        print(f'Download success => {file_name}_{count}.jpg')
                        if count > 1000:
                            break
            else:
                print('Download fail')
        
        except:
            pass

    cur_page += 1
    driver.quit()
    print("[next page]")

print(f"-[DONE]- {file_name}")