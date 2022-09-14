import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import secrets
import datetime 
from time import sleep
class database():
    def __init__(self):
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.ref = self.db.collection("fruit ninja")

    def get(self):
        query = self.db.collection("result").order_by(u'score' , direction=firestore.Query.DESCENDING).stream()
        return query

    def add(self , name , score):
        print(score)
        doc = {
            'name' : name,
            'score' : float(score)
        }
        self.db.collection("result").add(doc)

    def find(self , score):
        query = self.db.collection("result").where(u'score' , u'>=' , float(score)).order_by(u'score' , direction=firestore.Query.DESCENDING).stream()
        i = 0
        
        for doc in query:
            i += 1
        return i

    def update(self , score , id):
        self.ref.document(id).update({u'score':score})
        num = self.ref.document(id).get().to_dict()['room']

        peoples = self.db.collection("room").document(num).get().to_dict()['people']

        for people in peoples:
            if people == id : continue

            return self.ref.document(people).get().to_dict()['score']
            
    
    def search(self , num):
        id = secrets.token_urlsafe(8)+str(int(datetime.datetime.now().timestamp()))
        doc = {
            'score' : 0,
            'room' : str(num)
        }
        self.db.collection("fruit ninja").document(id).set(doc)

        query = self.db.collection("room").document(num).get()
        if query.exists:         
            self.db.collection("room").document(num).update({u'people' : firestore.ArrayUnion([id])})
            return id
        else:
            doc = {
                'people' : [id]
            }
            self.db.collection("room").document(num).set(doc)
            while len(self.db.collection("room").document(num).get().to_dict()['people']) == 1:
                query = self.db.collection("room").document(num).get()
                sleep(1)
            return id
        
    def close(self,num):
        self.db.collection("room").document(num).delete()

    def remove(self,num):
        self.ref.document(num).delete()