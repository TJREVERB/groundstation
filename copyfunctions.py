import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("groundstation-listen-log-firebase-adminsdk-h2jfr-9d71ce0bdb.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection(u'users').document(u'cubesat')
doc_ref.set({
    u'cubesat' : u'honorcode',
    u'year2' : 2022,
})
timestamp = "1/16 6:30"
city_ref = db.collection(u'users').document(u'cubesat')
city_ref.update({
    timestamp : 2020,
})