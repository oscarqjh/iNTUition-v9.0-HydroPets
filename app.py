#you need install pyrebase and uuid
from kivy.storage.dictstore import DictStore
import uuid
import pyrebase 
from datetime import datetime

config = {
  "apiKey": "BAhMFDARkFSb13VdVPjBuCxHR-5eZDNeWG6iSc39blazBa2nsbLFkD4YumGWLsXF5B-F-blUDGyM4xD_wpFrvpU",
  "authDomain": "waterapp-7e1ea.firebaseapp.com",
  "databaseURL": "https://waterapp-7e1ea-default-rtdb.asia-southeast1.firebasedatabase.app/",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



#user presses 'get started', generates a random unique id and registers an acc onto firebase, then authenticates the user and stores the unique id generated into the user's local cache
#not to be called directly
def _register():
    id = str(uuid.uuid4())
    store = DictStore(filename="MY_UNIQUE_ID")
    store.put("id", name=id)
    return id

#retrieves id in device storage, if don't have, register one; if have, then authenticate to database
def authenticate():
    try:
        store = DictStore(filename="MY_UNIQUE_ID")
        retrievedid = store.get("id")
        if not retrievedid: 
            retrievedid = _register()
        token = auth.create_custom_token(retrievedid)
        user = auth.sign_in_with_custom_token(token)
        data = {"time_to_water":datetime.now()}
        db.child("users").child(str(user)).set(data)
        return True
    except:
        return False

#returns true if it is past the time to drink, else false. before it returns true it sets time_to_water to next timing
def check_drink_time(user_id,db):
    hours=datetime.timedelta(minutes=60)
    ct = datetime.now()
    ud = db.child("users").get().val()[id]
    if not ud:
        return False
    if ct>= ud["time_to_water"]:
        data = {"time_to_water":datetime.now()+hours}
        db.child("users").child(user_id).set(data)
        return True
    return False