import tcpserver
import socketserver
import socket
import datetime
import json

textmessages = []


def get_request(data: dict, request: socket.socket):
    path = data[b'GET'].split(b' ', 1)[0]
    path: bytes

    response = b'HTTP/1.1 200 OK\r\n'
    response += b'Content-Type: text/html\r\n'
    response += b'X-Content-Type-Options: nosniff\r\n'

    if path == b'/':
        file = open('index.html', 'rb')
        html = file.read()
        file.close()
        response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
        response += html
        request.sendall(response)

    elif path == b'/ajax_get.html':
        file = open('ajax_get.html', 'rb')
        html = file.read()
        file.close()
        response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
        response += html
        request.sendall(response)

    elif path == b'/ajax_get_script.js':
        file = open('ajax_get_script.js', 'rb')
        js = file.read()
        file.close()

        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/javascript\r\n'
        response += b'X-Content-Type-Options: nosniff\r\n'
        response += b'Content-Length: ' + str(len(js)).encode() + b'\r\n\r\n'
        response += js
        request.sendall(response)

    elif path == b'/get_time':
        date = datetime.datetime.today()
        date = str(date).encode()

        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/plain\r\n'
        response += b'X-Content-Type-Options: nosniff\r\n'
        response += b'Content-Length: ' + str(len(date)).encode() + b'\r\n\r\n'
        response += date
        request.sendall(response)

    elif path == b'/ajax_post_get.html':
        file = open('ajax_post_get.html', 'rb')
        html = file.read()
        file.close()
        response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
        response += html
        request.sendall(response)

    elif path == b'/ajax_post_get_script.js':
        file = open('ajax_post_get_script.js', 'rb')
        js = file.read()
        file.close()

        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/javascript\r\n'
        response += b'X-Content-Type-Options: nosniff\r\n'
        response += b'Content-Length: ' + str(len(js)).encode() + b'\r\n\r\n'
        response += js
        request.sendall(response)

    elif path.startswith(b'/messages'):
        row = path.split(b'/messages')[1]
        if not row.isdigit() or int(row) >= len(textmessages):
            response = b'HTTP/1.1 204 No Content\r\n'
            request.sendall(response)
            return
        row = int(row)

        data = textmessages[row:]
        data_dict = {'userName': [], 'message': [], 'time': []}

        for element in data:
            data_dict['userName'].append(element[0])
            data_dict['message'].append(element[1])
            data_dict['time'].append(element[2])
        data = json.dumps(data_dict).encode()

        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/plain\r\n'
        response += b'X-Content-Type-Options: nosniff\r\n'
        response += b'Content-Length: ' + str(len(data)).encode() + b'\r\n\r\n'
        response += data
        request.sendall(response)

    elif path == b'/ajax_polling.html':
        file = open('ajax_polling.html', 'rb')
        html = file.read()
        file.close()
        response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
        response += html
        request.sendall(response)

    elif path == b'/ajax_polling_script.js':
        file = open('ajax_polling_script.js', 'rb')
        js = file.read()
        file.close()

        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/javascript\r\n'
        response += b'X-Content-Type-Options: nosniff\r\n'
        response += b'Content-Length: ' + str(len(js)).encode() + b'\r\n\r\n'
        response += js
        request.sendall(response)