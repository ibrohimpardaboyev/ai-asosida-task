import requests
import logging 
from datetime import timedelta
import datetime
import matplotlib.pyplot as plt
from ai_response import request_message_to_ai

logging.basicConfig(filename="logger.log",level=logging.INFO)

class WheatherApi:
    def __init__(self,currendateurl,history_url):
        self.current=currendateurl
        self.history_url = history_url
    def get_current_whether(self,**kwargs):
        resp = requests.get(self.current,params=kwargs).json()
        try:
            temp = resp['current']['temp_c']
            humidity = resp['current']['humidity']
            wind_degree=[resp['current']['wind_mph'],resp['current']['wind_kph']]
            return [temp,humidity,wind_degree]
        except Exception as e:
            logging.info(f"Error - {e}")
    def history_data(self,**kwargs):
        resp = requests.get(self.history_url,params=kwargs).json()
        try:
            forecast=resp["forecast"]['forecastday'][0]["day"]
            return ({
                "max_temp": forecast['maxtemp_c'],
                "min_temp": forecast['mintemp_c'],
                "avg_temp": forecast['avgtemp_c']
            })
        
        except Exception as e:
            logging.info(f"Error - {e}")
            print(e)
    
class HistoricWhetherPrediction:
    def __init__(self,q):
        self.week_data = {}
        self.city=q
        today = datetime.date.today()
        whetherapi = WheatherApi("http://api.weatherapi.com/v1/current.json","http://api.weatherapi.com/v1/history.json")
        for i in range(0,8):
            curr_date=today+timedelta(days=-i)
            dt_whether=whetherapi.history_data(key="2f6c8bb4e5714169a21164829250605",q=q,dt=curr_date)
            self.week_data[curr_date.strftime("%Y-%m-%d")] = dt_whether
    def predict_next_3_days_data(self):
        msg = f"{self.week_data} this is last weeks whether data for {self.city} Predict the next 3 days whether temperature based on this data" 
        resp = request_message_to_ai(msg)
        return resp
    def vizulize_data(self):
        data=self.week_data
        keys=[]
        values=[]
        for k,v in data.items():
            keys.append(k)
            values.append(v['avg_temp'])
            # temp[k] = v['avg_temp']
        keys=[datetime.datetime.strptime(x,"%Y-%m-%d").strftime("%A") for x in keys]
        plt.plot(keys,values)

        
            

# whetherapi = WheatherApi("http://api.weatherapi.com/v1/current.json","http://api.weatherapi.com/v1/history.json")
# curr=whetherapi.get_current_whether(key="2f6c8bb4e5714169a21164829250605",q="Tashkent")
# curr1=whetherapi.history_data(key="2f6c8bb4e5714169a21164829250605",q="Tashkent",dt="2025-05-05")

hist_data = HistoricWhetherPrediction("Tashkent")
print(hist_data.predict_next_3_days_data())
hist_data.vizulize_data()
