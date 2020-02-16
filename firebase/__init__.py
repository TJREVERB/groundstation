import firebase_admin
from firebase_admin import db, credentials


class Database:

    def __init__(self, creds: str, database_url: str, update_callback: callable):
        firebase_admin.initialize_app(credentials.Certificate(creds), {"databaseURL": database_url})
        self.reference = db.reference('/')
        self.reference.listen(update_callback)

    def read(self, path):
        return self.reference.child(path).get()


update_event = firebase_admin.db.Event
