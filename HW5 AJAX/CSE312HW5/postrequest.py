import tcpserver
import socketserver
import socket
import getrequest
import json
import datetime


def post_request(data: dict, request: socket.socket, post_data: bytes = None):
    path = data[b'POST'].split(b' ', 1)[0]
    content_length = int(data.get(b'Content-Length:'))
    post_data_length = len(post_data)

    while post_data_length < content_length:
        post_data += request.recv(4096).strip()
        post_data_length = len(post_data)

    if path == b'/message':

        post_data = post_data.decode('utf-8')
        post_data = post_data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        data_dict = json.loads(post_data)
        date = datetime.datetime.today()
        date = str(date)
        data_tuple = (data_dict.get('userName'), data_dict.get('message'), date)
        getrequest.textmessages.append(data_tuple)

        response = b'HTTP/1.1 204 No Content\r\n'
        request.sendall(response)


