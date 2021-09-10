import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db
cred = credentials.Certificate("credentials/firebaseConfig.json")
# Sets up Firebase app with credentials
app = firebase_admin.initialize_app(cred)

store = firestore.client()  # Used to access FireStore


def append_to_lst(collection: str, document: str, field: str, val) -> bool:
    """
    Add a value to a list in firebase
    """
    firebase_dict = store.collection(
        collection).document(document).get().to_dict()
    firebase_dict[field].append(val)
    store.collection(collection).document(document).set(firebase_dict)
    return True


def set_value(collection: str, document: str, field: str, val) -> bool:
    """
    Set a variable to value in firebase
    """
    firebase_dict = store.collection(
        collection).document(document).get().to_dict()
    firebase_dict[field] = (val)
    store.collection(collection).document(document).set(firebase_dict)
    return True


def get_value(collection: str, document: str, field: str):
    """
    Returns a value from firebase
    """
    return(store.collection(collection).document(document).get().to_dict()[field])
