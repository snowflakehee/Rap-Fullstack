from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("amazon.books.json", "r", encoding="utf-8") as f:
    books_data = json.load(f)

def is_match(book, query):
    query = query.lower()
    for key, value in book.items():
        if isinstance(value, list):
            value = " ".join(str(v).lower() for v in value)
        else:
            value = str(value).lower()
        if query in value:
            return True
    return False

def filter_books(data, query):
    if not query.strip():
        return data
    filters = query.split()
    result = []
    for book in data:
        if all(is_match(book, f) for f in filters):
            result.append(book)
    return result

@app.get("/")
def root():
    return {"message": "Book Search Engine is live"}

@app.get("/books/search")
def search_books(q: Optional[str] = Query("")):
    try:
        filtered = filter_books(books_data, q)
        return {"total": len(filtered), "results": filtered}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/books/suggestions")
def get_suggestions(q: Optional[str] = Query("")):
    suggestions = set()
    q_lower = q.lower()
    for book in books_data:
        title = book.get("title", "").lower()
        if q_lower in title:
            suggestions.add(book.get("title"))
        if len(suggestions) >= 10:
            break
    return {"suggestions": list(suggestions)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
