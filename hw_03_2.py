import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from pymongo import MongoClient

BASE_URL = "http://quotes.toscrape.com"
authors_data = []
quotes_data = []
visited_authors = set()

client = MongoClient("mongodb+srv://moonkaguia:<db_password>@nataliia-kaguia.qzoizac.mongodb.net/")
db = client["quotes_db"]
quotes_col = db["quotes"]
authors_col = db["authors"]

def get_author_details(url):
    response = requests.get(BASE_URL + url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    fullname = soup.find("h3", class_="author-title").text.strip()
    born_date = soup.find("span", class_="author-born-date").text.strip()
    born_location = soup.find("span", class_="author-born-location").text.strip()
    description = soup.find("div", class_="author-description").text.strip()

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

def scrape_quotes():
    page = 1
    while True:
        response = requests.get(f"{BASE_URL}/page/{page}/")
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")
        for quote in quotes:
            text = quote.find("span", class_="text").text.strip()
            author = quote.find("small", class_="author").text.strip()
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]

            quotes_data.append({
                "tags": tags,
                "author": author,
                "quote": text
            })

            author_href = quote.find("a")["href"]
            if author not in visited_authors:
                author_details = get_author_details(author_href)
                authors_data.append(author_details)
                visited_authors.add(author)
                sleep(0.2)  # Не спамити сервер

        page += 1

    # Збереження в JSON
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=2)

    print("✅ Дані збережено у quotes.json і authors.json")

    # Завантаження JSON
    with open("quotes.json", encoding="utf-8") as f:
         quotes = json.load(f)
    with open("authors.json", encoding="utf-8") as f:
         authors = json.load(f)

    # Завантаження у MongoDB
    quotes_col.insert_many(quotes)
    authors_col.insert_many(authors)

    print("✅ Дані імпортовано до MongoDB Atlas")

if __name__ == "__main__":
    scrape_quotes()
