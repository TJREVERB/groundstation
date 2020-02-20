from firebase import Database, update_event
import types
import validations
from radios import APRS


class GroundStation(Database):

    def __init__(self, database_credentials: str, database_url: str, receive_path: str, dispatch_path: str):
        self.receive_path = receive_path
        self.dispatch_path = dispatch_path
        super().__init__(database_credentials, database_url, self.on_update)
        self.received = self.reference.child(receive_path)
        self.sent = self.reference.child(dispatch_path)
        self.listen_list = []
        self.aprs = APRS(self.listen_list)

    def get_all_received(self):
        self.received = self.aprs.get_list()
        return self.received.get()

    def get_all_dispatched(self):
        return self.sent.get()


    #@validate(schema='received', position=3)
    #def add_new_received(self, message_type: ReceivedType, timestamp: int, data: dict):
        #self.received.child(message_type.value).child(f"{timestamp}").set(data)

    def on_update(self, event: update_event):
        if self.receive_path in event.path:
            print(f"New Received: {event.data}")
        elif self.dispatch_path in event.path:
            print(f"New Dispatched: {event.data}")
