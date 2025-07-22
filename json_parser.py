import json
import mysql.connector
from datetime import datetime

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="heera2202",
        database="food"
    )
    mycursor = mydb.cursor()

    with open("amazon.books.json", encoding="utf-8") as f:
        data = json.load(f)

    sql = """
    INSERT INTO books (
        id, title, isbn, pageCount, publishedDate, thumbnailUrl,
        shortDescription, longDescription, authors, categories
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for book in data:
        pub_date = None
        try:
            pub_date_str = book.get("publishedDate", {}).get("$date", None)
            if pub_date_str:
                pub_date = datetime.strptime(pub_date_str[:10], "%Y-%m-%d")
        except:
            pub_date = None

        val = (
            book.get("_id"),
            book.get("title"),
            book.get("isbn"),
            book.get("pageCount"),
            pub_date,
            book.get("thumbnailUrl"),
            book.get("shortDescription"),
            book.get("longDescription"),
            json.dumps(book.get("authors", [])),
            json.dumps(book.get("categories", []))
        )

        try:
            mycursor.execute(sql, val)
            print(f"Inserted: {book.get('title')}")
        except Exception as e:
            print(f"Error inserting '{book.get('title')}': {e}")

    mydb.commit()

except Exception as e:
    print(f"MySQL Error: {e}")

finally:
    mycursor.close()
    mydb.close()
    print("Connection closed")
