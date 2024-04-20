import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.yellowpages-uae.com/uae/restaurant"
output_restaurants = 1317 // 20
counter = 0
restaurants = []

for i in range(1, output_restaurants - 1):
    response = requests.get(f"{URL}-{i}.html")
    
    soup = BeautifulSoup(response.content, "html.parser")
    listings = soup.find_all(name="div", id="listings")
    
    for item in listings:

        names = [name.text.strip() for name in item.find_all(name="h2", id="name")]
        locations = [location.text.strip('Location : "" ') for location in item.find_all(name="span", class_="location")]
        cities = [city.text.strip('City : "" ') for city in item.find_all(name="span", class_="locationCity")]
        po_box_numbers = [po_box.text.strip() for po_box in item.find_all(name="span", class_="pobox")]
        links = [f'https://www.yellowpages-uae.com{link.get("onclick").strip("window.open () '' , _self")}l' for link in item.find_all(name="button", class_="more-info")]
        logo_links = [logo.get("data-src") for logo in item.find_all(name="img")]

        phone_numbers = []
        mobile_numbers = []
        for num in item.find_all(name="span", class_="phonespn"):
            if num.text[0] == "P":
                phone_numbers.append(num.text.strip("Call 800MIYABI , Phone :"))
            elif num.text[0] != "P":
                mobile_numbers.append(f'{num.text.strip("Call 800MIYABI , Mobile :")}')
            elif num.text == "P" and num.text == None:
                phone_numbers.append(None)
            elif num.text != "P" and num.text == None:
                mobile_numbers.append(None)


        try:
            for i in range(0, counter):
                restaurants.append({
                    "Name": names[i],
                    "Location": locations[i],
                    "City": cities[i],
                    "P.0 Box": po_box_numbers[i],
                    "Phone": phone_numbers[i],
                    "Mobile": mobile_numbers[i],
                    "Company page link": links[i],
                    "Logo url": logo_links[i]
                })
        except IndexError:
            restaurants[i]["Mobile"] = None
        
        counter += 1

        df = pd.DataFrame(restaurants)
        df.to_csv("results.csv", index=False)

        if counter == 1317:
            break
