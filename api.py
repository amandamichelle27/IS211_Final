# Standard library imports.
from json import load
from urllib2 import quote, urlopen

# The base URL pattern to generate requests.
url = "https://www.googleapis.com/books/v1/volumes?q=%s:%s"

# The default image to use for a thumbnail.
default_img = "https://i.imgur.com/tqe9vLl.png"


def search_books(type, value):
    return [{
        "title":      book["volumeInfo"].get("title"),
        "author":     book["volumeInfo"].get("authors", [None])[0],
        "page_count": book["volumeInfo"].get("pageCount"),
        "avg_score":  book["volumeInfo"].get("averageRating"),
        "thumbnail":  book["volumeInfo"].get(
                          "imageLinks", {}).get("thumbnail", default_img),
    }
    for book in load(urlopen(url % (type, quote(value)))).get("items", [])]