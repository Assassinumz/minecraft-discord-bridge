import time
from enum import Enum
import logging

import requests


class ElasticsearchLogger():
    def __init__(self, url: str, username: str = "", password: str = ""):
        self.url = url
        self.username = username
        self.password = password
        self.log = logging.getLogger("bridge.elasticsearch")

    def log_connection(self, uuid, reason, count=0):
        if ConnectionReason(reason).name != "SEEN":
            es_payload = {
                "uuid": uuid,
                "time": (lambda: int(round(time.time() * 1000)))(),
                "reason": ConnectionReason(reason).name,
                "count": count,
            }
        else:
            es_payload = {
                "uuid": uuid,
                "time": (lambda: int(round(time.time() * 1000)))(),
                "reason": ConnectionReason(reason).name,
            }
        self.post_request("connections/_doc/", es_payload)

    def log_chat_message(self, uuid, display_name, message, message_unformatted):
        es_payload = {
            "uuid": uuid,
            "display_name": display_name,
            "message": message,
            "message_unformatted": message_unformatted,
            "time": (lambda: int(round(time.time() * 1000)))(),
        }
        self.post_request("chat_messages/_doc/", es_payload)

    def log_raw_message(self, msg_type, message):
        es_payload = {
            "time": (lambda: int(round(time.time() * 1000)))(),
            "type": msg_type,
            "message": message,
        }
        self.post_request("raw_messages/_doc/", es_payload)

    def post_request(self, endpoint, payload):
        the_url = "{}{}".format(self.url, endpoint)
        if self.username and self.password:
            post = requests.post(the_url, auth=(self.username, self.password), json=payload)
        else:
            post = requests.post(the_url, json=payload)
        self.log.debug(post.text)


class ConnectionReason(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    SEEN = "SEEN"