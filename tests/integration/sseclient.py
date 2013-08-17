import socket
import re


def receive_headers(my_rfile):
    end_of_headers = False
    while not end_of_headers:
        data = my_rfile.readline(65536).decode("utf-8").rstrip()
        print("Header line: %s." % data)
        match = re.search(r"^HTTP/[0-9]\.[0-9] ([0-9]+) ([A-Z]+)", data)
        if match:
            status = match.group(1)
        if data == "":
            end_of_headers = True
    return status


def receive_sse_message(my_rfile):
    end_of_message = False
    while not end_of_message:
        data = my_rfile.readline(65536).decode("utf-8").rstrip()
        match = re.search(r"id: ([0-9]+)", data)
        if match:
            my_ident = int(match.group(1))
            print("ID: %s." % ident)
        match = re.search(r"event: (\S+)", data)
        if match:
            my_eventtype = match.group(1)
            print("Eventtype: %s." % eventtype)
        match = re.search(r"data: (.*)", data)
        if match:
            my_message_data = match.group(1)
            print("Data: %s." % message_data)
        if data == "":
            end_of_message = True
    return (my_ident, my_eventtype, my_message_data)

url = "http://barn.ewi.utwente.nl:6789"
url_parts = re.split(r"^(?:(https?)://)?((?:[\w]+\.)*[\w]+)(?::([0-9]+))?(\S*)", url)
if url_parts[3] == None:
    url_parts[3] = 80
events = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
events.connect((url_parts[2], int(url_parts[3])))
rfile = events.makefile('rb', -1)
wfile = events.makefile('wb', 0)
wfile.write(b"GET /events HTTP/1.1\r\nCache-Control: no-cache\r\n"
            b"Accept: text/event-stream\r\n\r\n")
wfile.flush()  # pylint: disable=E1103
if receive_headers(rfile) == "200":
    messages_received = 0
    while True:
        messages_received += 1
        ident, eventtype, message_data = receive_sse_message(rfile)
        print("Message %s: ID=%s, type=%s, data=%s." % (messages_received,
                                                        id, eventtype,
                                                        message_data))
rfile.close()
wfile.close()
