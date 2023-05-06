# import requests

# url = "https://m.media-amazon.com/images/I/81vDZyJQ-4L._AC_UY218_.jpg"
# response = requests.get(url)

# with open("image.jpg", "wb") as f:
#     f.write(response.content)
import requests
from bs4 import BeautifulSoup
import random
import time

# list of user agents to randomly choose from
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
]

brands = ['Samsung', 'Apple', 'OnePlus', 'Xiaomi']  # list of brands to search
model_ram_rom = {'Samsung Galaxy S21': {'ram': None, 'rom': None},
                 'iPhone 12': {'ram': None, 'rom': None},
                 'OnePlus 9 Pro': {'ram': None, 'rom': None},
                 'Xiaomi Mi 11': {'ram': None, 'rom': None}}  # dictionary of model names and RAM/ROM details
mobile_data = []  # list to store the scraped mobile data

for brand in brands:
    url = f'https://www.amazon.com/s?k={brand}+mobile'
    headers = {'User-Agent': random.choice(user_agents)}  # randomly choose a user agent
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    for r in results:
        title = r.find('h2').text.strip()
        price = r.find('span', {'class': 'a-offscreen'})
        if price:
            price = price.text
        else:
            price = 'Price not available'
        rating = r.find('span', {'class': 'a-icon-alt'})
        if rating:
            rating = rating.text
        else:
            rating = 'No rating available'
        
        # check if the current mobile is one of the specified models
        for model in model_ram_rom:
            if model in title:
                ram_rom = r.find('span', {'class': 'a-size-base-plus a-color-secondary a-text-normal'})
                if ram_rom:
                    ram_rom = ram_rom.text.strip().split('|')
                    model_ram_rom[model]['ram'] = ram_rom[0].strip()
                    model_ram_rom[model]['rom'] = ram_rom[1].strip()
                else:
                    model_ram_rom[model]['ram'] = 'RAM not available'
                    model_ram_rom[model]['rom'] = 'ROM'

print(mobile_data)
print(model_ram_rom)
