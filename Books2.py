from typing import Optional
from fastapi import FastAPI,Body

from  pydantic import BaseModel,Field

app = FastAPI()

class  Book:
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date  : int


    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):

    id : Optional[int] = Field(description="This field is optional",default=None)
    title : str = Field(min_length=3,max_length=15)
    author : str = Field(min_length=3,max_length=20)
    description : str = Field(min_length=5,max_length=50)
    rating : int = Field(gt=-1,lt=6)
    published_date : int = Field(gt=1990,lt=2030)

    model_config = {
        
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Mostafa",
                "description": "A new description of a book",
                "rating": 5,
                "published_date" : 2025
            }
        }
    }


Books = [
    Book(1,'title1','author1','desc1',3,2024),
    Book(2,'title2','author2','desc1',3,2021),
    Book(3,'title3','author3','desc1',3,2022),
    Book(4,'title4','author4','desc1',3,2000)
]

@app.get('/allbooks/')
async def read_all_books():
    return Books

#@app.post('/book/create/')
#def create_book(book_request = Body()):
#    Books.append(book_request)

@app.get("/books/publish/")
async def read_book_by_publish(published_date:int):
    Books_by_published = []
    for book in Books:
        if book.published_date == published_date:
            Books_by_published.append(book)
    return Books_by_published


@app.post('/book/create/')
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    Books.append(find_book_id(new_book))


def find_book_id(book:Book):
    book.id =1 if len(Books)<0 else Books[-1].id + 1
    return book

@app.get('/book/{book_id}')
async def  read_book(book_id:int):
    for book in Books :
        if book.id == book_id :
            return book
        

@app.get('/book/')
async def read_book_by_rating(book_rating : int):
    Books_by_rating = []
    for book in Books:
        if book.rating == book_rating:
            Books_by_rating.append(book)
    return Books_by_rating

@app.put('/book/update_book/')
async def update_book(book:BookRequest):
    for i in range(len(Books)):
        if Books[i].id  == book.id:
            Books[i] = book


@app.delete('/book/delete_book/')
async def deletebook(book_id:int):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            break   