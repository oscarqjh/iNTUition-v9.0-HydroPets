#you need install pyrebase and uuid
from kivy.storage.dictstore import DictStore
import uuid
from datetime import datetime,timedelta
import time
import requests
import threading
from pyfcm import FCMNotification

config = {
  "apiKey": "BAhMFDARkFSb13VdVPjBuCxHR-5eZDNeWG6iSc39blazBa2nsbLFkD4YumGWLsXF5B-F-blUDGyM4xD_wpFrvpU",
  "authDomain": "waterapp-7e1ea.firebaseapp.com",
  "databaseURL": "https://waterapp-7e1ea-default-rtdb.asia-southeast1.firebasedatabase.app/",
}

firebase = "https://waterapp-7e1ea-default-rtdb.asia-southeast1.firebasedatabase.app/users.json"
api_key = "AIzaSyC58TtIJ_0AsJR1BvTu9wn4ShPSjOMQX0k"
push_service = FCMNotification(api_key=api_key)



#user presses 'get started', generates a random unique id and registers an acc onto firebase, then authenticates the user and stores the unique id generated into the user's local cache
#not to be called directly
def _register():
    id = str(uuid.uuid4())
    store = DictStore(filename="MY_UNIQUE_ID")
    authenticate_link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    stat = requests.post(url=authenticate_link)
    print(stat.text)
    store.put("id", name=stat.json()["localId"])
    return store.get("id")["name"]

def _putToDB(nojsondata,userid):
     firebase = f"https://waterapp-7e1ea-default-rtdb.asia-southeast1.firebasedatabase.app/users/{userid}.json"
     res = requests.put(url=firebase,json=nojsondata)
     return res.status_code==200

def _getFromDB(datakey="time_to_water",userid=None):
     if not userid and datakey: return
     firebase = f"https://waterapp-7e1ea-default-rtdb.asia-southeast1.firebasedatabase.app/users/{userid}.json"
     res = requests.get(url=firebase)
     return res.json()[datakey]
     

#retrieves id in device storage, if don't have, register one; if have, then authenticate to database
def authenticate():
        store = DictStore(filename="MY_UNIQUE_ID")
        if not store.store_exists("id"):
            _register()
        data = {"time_to_water":str(time.time_ns()//100000)}
        userid = store.get("id")["name"]
        _putToDB(data,userid)
        return True

#returns true if it is past the time to drink, else false. before it returns true it sets time_to_water to next timing
def check_drink_time(user_id):
    hour = 3600
    ct = time.time_ns()//100000
    ud = int(_getFromDB("time_to_water",user_id))
    print(ud)
    if not ud:
        return False
    if ct-ud>=hour:
        data = {"time_to_water":str(time.time_ns()//100000)}
        _putToDB(data)
        return True
    return False


def set_interval(f, sec):
    def looper():
        set_interval(f, sec)
        f()
    timer = threading.Timer(sec, looper)
    timer.start()
    return timer