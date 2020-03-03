import socket
import base64
import json
import mimetypes
import datetime
import pickle

import os
from threading import Thread
from pytz import timezone

from email import message_from_string, encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from googleapiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class APRS:
    """
    Listen class used as object in main.py 
    Allows for threading to listen
    Returns all messages received
    """

    def __init__(self, call_back: callable):
        self.callback = call_back
        self.start_thread()

    def start_thread(self):
        """
        Starts a thread to listen for new messages
        """
        listen_thread = Thread(target=self.run, args=())
        listen_thread.daemon = True
        listen_thread.start()

    def run(self):
        """
        Thread that continiously listens for new messages using sockets
        Adds the received message to the message list
        Checks to see if message was sent by us
        """
        UDP_ID = "127.0.0.1"
        RX_PORT = 5557
        while True:
            msg_lstn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msg_lstn.bind((UDP_ID, RX_PORT))
            message_received = msg_lstn.recvfrom(1024)
            if "to SATT4" in str(message_received):
                self.callback(message_received)
                
    def send(self, msg: str):
        """
        Given a message, simply generates checksum and sends message
        Does not check anything
        Returns true if message successfully sent
        Returns false if message not sent
        """
        tx_port = 5555
        udp_ip = "127.0.0.1"
        try:  # Message successfully sent
            msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msg_snd.sendto(msg.encode(), (udp_ip, tx_port))
            return True
        except:
            return False


class Iridium:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send',
                       'https://www.googleapis.com/auth/gmail.modify']
        self.SECRETS_FILENAME = "credentials.json"
        self.SECRETS_FILENAME_ENCRYPTED = "credentials.json.gpg"
        self.IMEI = None

        self.MSG_FILENAME_DEFAULT = "msg.sbd"

        self.MAIL_TO_SEND = "data@sbd.iridium.com"
        self.MAIL_FROM = "tjreverb@gmail.com"

        self.MAIL_RECEIVE = "sbdservice@sbd.iridium.com"
        self.MAIL_RECEIVE_SUBJECT = "SBD Msg From Unit: "
        #start listen thread
        
    def check_secrets_exists(self) -> bool:
        if os.path.exists(self.SECRETS_FILENAME):
            return True
        elif os.path.exists(self.SECRETS_FILENAME_ENCRYPTED):
            return False
        else:
            return False

    def get_imei(self) -> int:
        if self.check_secrets_exists():
            with open(self.SECRETS_FILENAME) as f:
                data = json.load(f)

            imei = data["imei"]

            return imei

    def get_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

        return service

    def main(self):
        """
        Needs to be maanually required
        """
        #global IMEI, MAIL_RECEIVE_SUBJECT
        self.IMEI = self.get_imei()
        self.MAIL_RECEIVE_SUBJECT += str(self.IMEI)

    def send(self, use_msg, use_file, body):
        service = self.get_service()

        if use_msg:
            self.create_msg_file(body)
            self.send_mail(self.MSG_FILENAME_DEFAULT, service)
            delete_msg_file()
        elif use_file:
            if not os.path.exists(body):
                return
            if not body.endswith(".sbd"):
                return
            self.send_mail(body, service)
        else:
            self.create_msg_file(body)
            self.send_mail(self.MSG_FILENAME_DEFAULT, service)
            self.delete_msg_file()

    def send_mail(self, msg_filename, service):
        message = MIMEMultipart()
        message["to"] = self.MAIL_TO_SEND
        message["from"] = self.MAIL_FROM
        message["subject"] = str(self.IMEI)

        mail_body = MIMEText("")
        message.attach(mail_body)

        content_type, encoding = mimetypes.guess_type(msg_filename)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        file_attachment = open(msg_filename, 'rb')
        mail_attachment = MIMEBase(main_type, sub_type)
        mail_attachment.set_payload(file_attachment.read())
        encoders.encode_base64(mail_attachment)
        file_attachment.close()

        filename = os.path.basename(msg_filename)
        mail_attachment.add_header(
            'Content-Disposition', 'attachment', filename=filename)
        message.attach(mail_attachment)

        # Create the encoded message
        message_encoded = {'raw': base64.urlsafe_b64encode(
            message.as_bytes()).decode()}

        try:
            message = (service.users().messages().self.send(userId=self.MAIL_FROM, body=message_encoded)
                       .execute())
            return message
        except errors.HttpError as error:
            return

    def create_msg_file(self, msg):
        self.delete_msg_file()
        msg_file = open(self.MSG_FILENAME_DEFAULT, "w+")
        msg_file.write(msg)
        msg_file.close()

    def delete_msg_file(self):
        if os.path.exists(self.MSG_FILENAME_DEFAULT):
            os.remove(self.MSG_FILENAME_DEFAULT)
        else:
            return  # error

    def receive(self, num_msgs):
        service = self.get_service()
        query = "from:" + self.MAIL_RECEIVE + " " \
                + "subject:" + self.MAIL_RECEIVE_SUBJECT + " " \
                + "has:attachment"
        messages = self.receive_msg_list(
            service, self.MAIL_FROM, num_msgs, query)

        for message in messages:
            msg_body = str(self.receive_msg_body(
                service, self.MAIL_FROM, message["id"]))
            msg_decoded = self.receive_msg_attach(
                service, self.MAIL_FROM, message["id"], "")
            if msg_decoded is not None or msg_decoded:
                """
                replace print with something meaningful
                """
                print(self.get_msg_send_date(
                    msg_body).strftime("%c"))
                print(msg_decoded)

    def receive_msg_list(self, service, user_id, max_results, query=''):
        """List all Messages of the user's mailbox matching the query.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            query: String used to filter messages returned.
            Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
            List of Messages that match the criteria of the query. Note that the
            returned list contains Message IDs, you must use get with the
            appropriate ID to get the details of a Message.
        """

        try:
            response = service.users().messages().list(userId=user_id,
                                                       q=query,
                                                       maxResults=max_results).execute()
            messages = []

            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user_id, q=query,
                                                           pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages[:max_results]

        except errors.HttpError as error:
            return  # error

    def receive_msg_body(self, service, user_id, msg_id):
        """Get a Message and use it to create a MIME Message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: The ID of the Message required.

        Returns:
            A MIME Message, consisting of data from Message.
        """

        try:
            message = service.users().messages().get(userId=user_id, id=msg_id,
                                                     format='raw').execute()

            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

            mime_msg = message_from_string(msg_str.decode())

            return mime_msg

        except errors.HttpError as error:
            print(error)

    def receive_msg_attach(self, service, user_id, msg_id, store_dir="msg", save=False):
        """Get and store attachment from Message with given id.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: ID of Message containing attachment.
            store_dir: The directory used to store attachments.
        """
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id).execute()

            for part in message['payload']['parts']:
                if part['filename']:
                    if 'data' in part['body']:
                        attach_data = part['body']['data']
                    else:
                        attach_id = part['body']['attachmentId']
                        attach = service.users().messages().attachments().get(userId=user_id, messageId=msg_id,
                                                                              id=attach_id).execute()
                        attach_data = attach['data']

                    file_data = base64.urlsafe_b64decode(attach_data
                                                         .encode('UTF-8'))

                    file_decoded_msg = file_data.decode()

                    if save:
                        file_local_path = ''.join(
                            [store_dir, part['filename']])

                        f = open(file_local_path, 'w')
                        f.write(file_decoded_msg)
                        f.close()

                    return file_decoded_msg

        except errors.HttpError as error:
            print(error)

    def get_msg_send_date(self, msg_body) -> datetime.datetime:
        date = ""
        for line in msg_body.split("\n"):
            if "Time of Session" in line:
                date = line.strip()

        date_string = date.replace("Time of Session (UTC): ", "")
        date_format = '%c'

        try:
            date_parsed = datetime.datetime.strptime(date_string, date_format)

            date_parsed_tz = date_parsed.replace(
                tzinfo=timezone("UTC")).astimezone(timezone("US/Eastern"))

            return date_parsed_tz
        except ValueError:
            print("error")
