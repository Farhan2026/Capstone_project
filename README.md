# Book Data Pipeline

An end-to-end Python project that scrapes the first 20 books from `books.toscrape.com`, stores them in SQLite, exposes them through a FastAPI service, and consumes the API in a client script that exports CSV data and generates a scatter plot.

## Features

- Scrapes book title, price, stock status, and rating.
- Stores data in an SQLite database with CRUD operations.
- Exposes REST endpoints through FastAPI.
- Loads API data into a Pandas DataFrame.
- Exports `exported_books.csv`.
- Generates `price_vs_rating.png`.

## Project Files

- `scraper.py` - Scrapes the first 20 books and loads them into SQLite.
- `database.py` - SQLite database manager with create, read, update, and delete methods.
- `main.py` - FastAPI application exposing the book endpoints.
- `client.py` - API client that prints the DataFrame, exports CSV, and creates the plot.

## Requirements

- Python 3.10 or later
- `requests`
- `beautifulsoup4`
- `fastapi`
- `uvicorn`
- `pandas`
- `matplotlib`

The project virtual environment already includes these dependencies.

## Setup

If you want to use the existing virtual environment:

```powershell
Set-Location C:\Users\Admin\CapstoneProject\book_pipeline
.\venv\Scripts\python.exe --version
```

## Run the Project

1. Populate the database with scraped data:

```powershell
Set-Location C:\Users\Admin\CapstoneProject\book_pipeline
.\venv\Scripts\python.exe scraper.py
```

2. Start the FastAPI server:

```powershell
Set-Location C:\Users\Admin\CapstoneProject\book_pipeline
.\venv\Scripts\python.exe -m uvicorn main:app --app-dir C:\Users\Admin\CapstoneProject\book_pipeline --host 127.0.0.1 --port 8000
```

3. Run the client script in another terminal:

```powershell
Set-Location C:\Users\Admin\CapstoneProject\book_pipeline
.\venv\Scripts\python.exe client.py
```

## API Endpoints

- `GET /books` - Retrieve all books.
- `GET /books/{book_id}` - Retrieve a single book by ID.
- `POST /books` - Create a new book.
- `PUT /books/{book_id}` - Update an existing book.
- `DELETE /books/{book_id}` - Delete a book.

## Output Files

- `books.db` - SQLite database created by the scraper and used by the API.
- `exported_books.csv` - CSV export created by `client.py`.
- `price_vs_rating.png` - Scatter plot created by `client.py`.

## Notes

- The scraper always loads only the first 20 books from the main page.
- The generated output files and the database are ignored by git because they are runtime artifacts.
- If you rerun the scraper, it refreshes the database before inserting the latest 20 books.