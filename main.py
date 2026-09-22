from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import BookDatabaseManager


app = FastAPI(title="Book Data Pipeline API")

database = BookDatabaseManager()


class Book(BaseModel):
    title: str
    price: float
    in_stock: bool
    rating: int = Field(ge=1, le=5)


@app.get("/books")
def get_books():
    return database.get_all_books()


@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = database.get_book(book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post("/books", status_code=201)
def create_book(book: Book):
    book_id = database.create_book(
        book.title,
        book.price,
        book.in_stock,
        book.rating
    )

    return {
        "id": book_id,
        "title": book.title,
        "price": book.price,
        "in_stock": book.in_stock,
        "rating": book.rating
    }


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    updated = database.update_book(
        book_id,
        book.title,
        book.price,
        book.in_stock,
        book.rating
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "message": "Book updated successfully",
        "id": book_id
    }


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    deleted = database.delete_book(book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "message": "Book deleted successfully",
        "id": book_id
    }