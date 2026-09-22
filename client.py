from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests


API_URL = "http://127.0.0.1:8000/books"
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "exported_books.csv"
PLOT_PATH = BASE_DIR / "price_vs_rating.png"


def fetch_books(api_url=API_URL):
	response = requests.get(api_url, timeout=10)
	response.raise_for_status()
	return response.json()


def build_dataframe(books):
	dataframe = pd.DataFrame(books)

	if dataframe.empty:
		return dataframe

	expected_columns = ["id", "title", "price", "in_stock", "rating"]
	dataframe = dataframe[[column for column in expected_columns if column in dataframe.columns]]

	return dataframe


def export_books(dataframe, csv_path=CSV_PATH):
	dataframe.to_csv(csv_path, index=False)


def create_scatter_plot(dataframe, plot_path=PLOT_PATH):
	if dataframe.empty:
		return

	plt.figure(figsize=(8, 6))
	plt.scatter(dataframe["price"], dataframe["rating"], alpha=0.75, color="#1f77b4")
	plt.title("Price vs Rating for Scraped Books")
	plt.xlabel("Price")
	plt.ylabel("Rating")
	plt.yticks([1, 2, 3, 4, 5])
	plt.grid(True, linestyle="--", alpha=0.3)
	plt.tight_layout()
	plt.savefig(plot_path, dpi=150)
	plt.close()


def main():
	books = fetch_books()
	dataframe = build_dataframe(books)

	print(dataframe.to_string(index=False))

	export_books(dataframe)
	create_scatter_plot(dataframe)

	print(f"Exported CSV to {CSV_PATH.resolve()}")
	print(f"Saved scatter plot to {PLOT_PATH.resolve()}")


if __name__ == "__main__":
	main()
