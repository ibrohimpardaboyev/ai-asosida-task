import pandas as pd
import requests 
from ai_response import request_message_to_ai
import logging 
import datetime
logging.basicConfig(filename="log.log",level=logging.INFO)

logging.info(f"program started at - {datetime.datetime.now()}")

class ApiClient:
    def __init__(self,url):
        self.url = url
    def search_book_by_subject(self,genre,**kwargs):
        post = requests.get(self.url+genre+'.json',kwargs)
        return post.json()
    def search_book_by_title(self,**kwargs):
        book_by_title = requests.get(self.url,kwargs)
        return book_by_title.json()
class User:
    def __init__(self,user_id: int)->None:
        self.session_id = user_id 
        df=pd.read_csv("users_book_read_data.csv")
        self.genres = []
        self.data = df[df['user_id']==user_id]
        for genre in self.data['genres']:
            self.genres.append(genre.replace("\"","").replace("'","").split(","))
    def read_books(self) -> list:
        return self.data['book_name'].to_list()
    def recommend_book(self):
        self.frequent_genres = {}
        # counts=[]
        for genre in self.genres:
            for i in genre:
                cnt = self.frequent_genres.get(i,0)+1
                self.frequent_genres[i] = cnt

        resp_from_ai = request_message_to_ai(f"users read book's genres: {self.frequent_genres} based on this genre frequency recommend a book to read only give book name and genre")
        logging.info(f"{resp_from_ai} is reccomended for the user with {self.session_id} user_id")
        return resp_from_ai
        
        

user = User(1)
user.read_books()
user.recommend_book()
logging.info(f"program ended at - {datetime.datetime.now()}")

# by_subject = ApiClient("https://openlibrary.org/subjects/")
# print(by_subject.search_book_by_subject("adventure",published_in="2025"))
# by_title = ApiClient("https://openlibrary.org/search.json").search_book_by_title(q="Harry Potter")
