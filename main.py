from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import setupdb
from routes.news import router as news_router


app = FastAPI(title="RSS Aggregator")

# Allow frontend (different port/origin) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run DB setup once when the app starts
setupdb()

# Plug in the /news endpoint
app.include_router(news_router)


@app.get("/")
def root():
    return {"status": "RSS Aggregator running"}



# from fastapi import FastAPI, Header
# from pydantic import BaseModel

# app = FastAPI()

# @app.get('/')
# def gettheword():
#         return{"hello"}
    
# @app.get('/gurt{name}')
# def yo(name:str):
#     return{"listen nigga": f"hello {name}"}

# class bookmodel(BaseModel):
#         title: str
#         name: str
        
# @app.post('/getting_book')
# async def debook(thebook: bookmodel):
#         return{
#                 "title" : thebook.title,
#                 "name" : thebook.name
#         }
        
# @app.get('/getting_headers')
# async def headers():

# from fastapi import FastAPI,Header
# from pydantic import BaseModel

# app = FastAPI()

# @app.get('/books')
# async def getting_all_books():
#         pass

# @app.post('/getbooks')
# async def creating_books():
#         pass
# @app.get('/books/{id}')
# async def findingbook_by_numbers(id: int):
#         pass

# @app.get('/get headers')
# async def getting_headers(
#         host:str = Header(None)
# ):
#         request_headers = {}
        
#         request_headers["Host"] = host 
        
#         return request_headers

# class bookmodel(BaseModel):
#         type: str
#         number: int

# from fastapi import FastAPI, status
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()

# class database(BaseModel):
#         name : str
#         number : int
#         address : str
        

# @app.get('/contacts',response_model= List[database])
# async def getting_contacts():
#         return database#not this something else

# @app.post('/create',status_code=status.HTTP_201_CREATED)
# async def creating_a_newline(data:database) -> 
#         pass

# @app.patch('/gettingbooks{book_id}')
# async def updatingbooks(book_id : int, ):
#         pass