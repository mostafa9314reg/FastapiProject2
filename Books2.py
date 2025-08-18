from fastapi import FastAPI,Body

from  pydantic import BaseModel

app = FastAPI()

class  Book:
    id : int
    title : str
    author : str
    description : str
    rating : int


    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):

    id : int 
    title : str
    author : str
    description : str
    rating : int


Books = [
    Book(1,'title1','author1','desc1',3),
    Book(2,'title2','author2','desc1',3),
    Book(3,'title3','author3','desc1',3),
    Book(4,'title4','author4','desc1',3)
]

@app.get('/allbooks/')
def read_all_books():
    return Books

#@app.post('/book/create/')
#def create_book(book_request = Body()):
#    Books.append(book_request)

@app.post('/book/create/')
def create_book(book_request :BookRequest):
    new_book = Book(**book_request.model_dump())
    Books.append(new_book)
