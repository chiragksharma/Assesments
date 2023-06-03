# Importing Libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#site%3Ayoutube.com+openinapp.co
# https://www.google.com/search?q=site%3Ayoutube.com+openinapp.co&start=1
website = 'https://www.google.com/search?q=site%3Ayoutube.com+openinapp.co&num=40000'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(website)

soup = BeautifulSoup(driver.page_source,"lxml")
num_pages = 3
youtube_channels = []
youtube_channel_name = []

for i in range(0 , num_pages - 1):
    items = soup.find_all('div', {'class': 'yuRUbf'})
    for item in items:
        link = item.a['href']
        if link.startswith('https://www.youtube.com/c/'):
            # youtube_channel_link = link.split('/url?q=')[1].split('&')[0]
            youtube_channels.append(link)
            name = link.split('/')[4]
            youtube_channel_name.append(name)

    nextButton = driver.find_element(By.LINK_TEXT , 'Next')
    nextButton.click()

youtube_channels=[*set(youtube_channels)]
youtube_channel_name = [*set(youtube_channel_name)]
print(youtube_channels)
print(youtube_channel_name)
# Save results in JSON format
with open('youtube_channels.json', 'w') as file:
    json.dump(youtube_channels, file)

# Save results in CSV format
with open('youtube_channels.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['YouTube Channel Links'])
    writer.writerows([[channel] for channel in youtube_channels])

with open('youtube_channel_names.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['YouTube Channel Names'])
    writer.writerows([[channel] for channel in youtube_channel_name])
while True:
    pass