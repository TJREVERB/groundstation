import firebase_admin
from firebase_admin import db, credentials


class Database:
    def __init__(self, creds: str, database_url: str, update_callback: callable, name=None):
        if(name is None):
            firebase_admin.initialize_app(credentials.Certificate(creds), {
                "databaseURL": database_url})
        else:
            firebase_admin.initialize_app(credentials.Certificate(creds), {
                "databaseURL": database_url}, name)
        self.reference = db.reference('/')
        self.reference.listen(update_callback)

    def read(self, path):
        return self.reference.child(path).get()

    def add_child(self, path, json):
        return self.reference.child(path).push(json)


update_event = firebase_admin.db.Event
