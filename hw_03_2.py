import requests
from bs4 import BeautifulSoup
import json
from time import sleep

BASE_URL = "http://quotes.toscrape.com"
quotes_data = []
authors_data = []
visited_authors = set()

def get_author_details(author_url):
    full_url = BASE_URL + author_url
    response = requests.get(full_url)
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

def scrape_site():
    page = 1
    while True:
        print(f"🔎 Скрапінг сторінки {page}...")
        response = requests.get(f"{BASE_URL}/page/{page}/")
        if response.status_code != 200:
            print("❌ Сторінку не знайдено. Завершення.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            print("📄 Цитат більше немає. Завершення.")
            break

        for quote in quotes:
            text = quote.find("span", class_="text").text.strip()
            author = quote.find("small", class_="author").text.strip()
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]

            quotes_data.append({
                "tags": tags,
                "author": author,
                "quote": text
            })

            author_link = quote.find("a")["href"]
            if author not in visited_authors:
                author_details = get_author_details(author_link)
                authors_data.append(author_details)
                visited_authors.add(author)
                sleep(0.1)

        page += 1

    print(f"✅ Зібрано {len(quotes_data)} цитат та {len(authors_data)} авторів")

    # Збереження в JSON
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=2)

    print("💾 Дані збережено у 'quotes.json' та 'authors.json'")

if __name__ == "__main__":
    scrape_site()
