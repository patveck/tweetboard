import socket
import re

def receive_headers(socket):
    end_of_headers = False
    while not end_of_headers:
        data = socket.recv(4096).decode("utf-8")
        match = re.search(r"^HTTP/[0-9]\.[0-9] ([0-9]+) ([A-Z]+)\r\n", data)
        if match:
            status = match.group(1)
        match = re.search(r"\r\n\r\n", data)
        if match:
            end_of_headers = True
    return status

def receive_sse_message(socket):
    end_of_message = False
    while not end_of_message:
        data = socket.recv(4096).decode("utf-8")
        match = re.search(r"id: ([0-9]+)\r\n", data)
        if match:
            id = int(match.group(1))
            print("ID: %s." % id)
        match = re.search(r"event: (\S+)\r\n", data)
        if match:
            eventtype = match.group(1)
            print("Eventtype: %s." % eventtype)
        match = re.search(r"data: (.*)\r\n", data)
        if match:
            message_data = match.group(1)
            print("Data: %s." % message_data)
        match = re.search(r"\r\n\r\n", data)
        if match:
            end_of_message = True
    return (id, eventtype, message_data)

url = "http://barn.ewi.utwente.nl:6789"
url_parts = re.split(r"^(?:(https?)://)?((?:[\w]+\.)*[\w]+)(?::([0-9]+))?(\S*)", url)
if url_parts[3] == None:
    url_parts[3] = 80
events = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
events.connect((url_parts[2], int(url_parts[3])))
events.sendall(b"GET /events HTTP/1.1\r\nCache-Control: no-cache\r\n"
               b"Accept: text/event-stream\r\n\r\n")
if receive_headers(events) == "200":
    messages_received = 0
    while True:
        messages_received += 1
        id, eventtype, message_data = receive_sse_message(events)
        print("Message %s: ID=%s, type=%s, data=%s." % (messages_received,
                                                        id, eventtype,
                                                        message_data))
events.close()

