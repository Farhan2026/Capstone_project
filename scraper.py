import requests
from bs4 import BeautifulSoup
from database import BookDatabaseManager
import re


URL = "https://books.toscrape.com/"


def scrape_books():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for article in soup.select("article.product_pod")[:20]:
        title = article.select_one("h3 a")["title"]

        price_text = article.select_one(".price_color").get_text(strip=True)
        price_match = re.search(r"\d+(?:\.\d+)?", price_text)
        price = float(price_match.group(0)) if price_match else 0.0

        availability = article.select_one(".availability").get_text(" ", strip=True)
        in_stock = "In stock" in availability

        rating_word = article.select_one(".star-rating")["class"][1]

        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        rating = rating_map[rating_word]

        books.append({
            "title": title,
            "price": price,
            "in_stock": in_stock,
            "rating": rating
        })

    return books


if __name__ == "__main__":
    books = scrape_books()

    database = BookDatabaseManager()
    database.clear_books()

    for book in books:
        database.create_book(
            book["title"],
            book["price"],
            book["in_stock"],
            book["rating"]
        )

    print(f"Successfully scraped and inserted {len(books)} books.")