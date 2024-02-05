import re
import bs4
import requests
import json
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from geopy.geocoders import Nominatim

#sends request to get the latitude and longitude of the International Space Station
req = requests.get('https://api.wheretheiss.at/v1/satellites/25544', timeout=3);
data = req.json();
latitude = float(data['latitude']);
longitude = float(data['longitude']);

print("ISS Latitude: ", latitude);
print("ISS Longitude: ", longitude);

#uses an API to locate which city, country and/or continent the coordinates point towards
req = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client?latitude="+str(latitude)+"&longitude="+str(longitude)+"&localityLanguage=en");
if req.status_code == 200:
    iss = req.json();
    if "GMT" in iss['locality'] or iss['locality'] =='':
        if "GMT" in iss['countryName'] or iss['countryName'] =='':
            if "GMT" in iss['continent'] or iss['continent'] =='':
                print()
                print("ISS location temporarily unavailable.");
            else:
                my_url = "https://en.wikipedia.org/wiki/"+iss['continent'];
                response = requests.get(my_url)

                #uses webscraping to get general info on the current location through Wikipedia
                if response.status_code == 200:
                    page_soup = soup(response.text, "html.parser")
                    paragraphs = page_soup.findAll('p')
                    filter_phrases = ["was the", "is the", "are the", "was a", "is a", "are a"]

                    for p in paragraphs:
                        paragraph_text = p.get_text().lower()
                        if any(phrase in paragraph_text for phrase in filter_phrases):
                            text_with_notations = p.get_text()
                            cleaned_text = re.sub(r'\[\d+\]', '', text_with_notations)
                            print()
                            print("The International Space Station is currently near "+iss['continent']);
                            print()
                            print(cleaned_text)
                            break
                else:
                    print()
                    print("The International Space Station is currently near "+iss['continent']);
        else:
            my_url = "https://en.wikipedia.org/wiki/"+iss['countryName'];
            response = requests.get(my_url)

            if response.status_code == 200:
                page_soup = soup(response.text, "html.parser")
                paragraphs = page_soup.findAll('p')
                filter_phrases = ["was the", "is the", "are the", "was a", "is a", "are a"]

                for p in paragraphs:
                    paragraph_text = p.get_text().lower()
                    if any(phrase in paragraph_text for phrase in filter_phrases):
                        text_with_notations = p.get_text()
                        cleaned_text = re.sub(r'\[\d+\]', '', text_with_notations)
                        print()
                        print("The International Space Station is currently near "+iss['countryName']);
                        print()
                        print(cleaned_text)
                        break
            else:
                print()
                print("The International Space Station is currently near "+iss['countryName']);
    else:
        my_url = "https://en.wikipedia.org/wiki/"+iss['locality'];
        response = requests.get(my_url)

        if response.status_code == 200:
            page_soup = soup(response.text, "html.parser")
            paragraphs = page_soup.findAll('p')
            filter_phrases = ["was the", "is the", "are the", "was a", "is a", "are a"]

            for p in paragraphs:
                paragraph_text = p.get_text().lower()
                if any(phrase in paragraph_text for phrase in filter_phrases):
                    text_with_notations = p.get_text()
                    cleaned_text = re.sub(r'\[\d+\]', '', text_with_notations)
                    print()
                    print("The International Space Station is currently near "+iss['locality']+", "+iss['countryName']+".");
                    print()
                    print(cleaned_text)
                    break
        else:
            print()
            print("The International Space Station is currently near "+iss['locality']+", "+iss['countryName']+".");
