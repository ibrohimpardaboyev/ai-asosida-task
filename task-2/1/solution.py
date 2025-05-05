from newsapi import NewsApiClient
import pandas as pd
import matplotlib.pyplot as plt
from sentimen_detector import sentiment
import seaborn as sns
import json
import asyncio
from ai_response import request_message_to_ai as ai_message
import datetime

class NewsAnalysis:
    def __init__(self):
        self.news = {}
        self.sentiments = {}
    def newapi(self,about:str):
        api = NewsApiClient(api_key='ac200126971b4e838e9b9e7d0737f355')
        data = api.get_everything(q=about)
            
        self.news = data['articles']
    def sentiment_analysis(self):
        for news in self.news:
            # print(news)
            msg = sentiment(news['title'])
            cnt=self.sentiments.get(msg,0)
            self.sentiments[msg] = cnt + 1
    def visaulize_sentiments(self):
        sns.barplot(x=self.sentiments.keys(),y=self.sentiments.values(),palette='Set2')
        # plt.title("Sentiment Counts")
    def save_to_json(self):
        with open("data.json","w") as file:
            json.dump(self.sentiments,file)
        print("data saved successfully")  
    
            
    
new = NewsAnalysis()
new.newapi(1)
new.sentiment_analysis()
new.visaulize_sentiments()
new.save_to_json()
