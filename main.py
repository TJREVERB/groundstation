from firebase import Database, update_event


def on_update(event: update_event):
    print(type(event))
    print(event.path, event.data)


CREDENTIALS = 'service_account_key.json'
DATABASE_URL = 'https://groundstation-ecf9f.firebaseio.com/'

db = Database(CREDENTIALS, DATABASE_URL, on_update)
print(db.read('messages/beacons').get())