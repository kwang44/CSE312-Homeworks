import tcpserver
import socketserver
import socket
import os.path
from os import path
from urllib.parse import unquote_to_bytes

images_dict = {}

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

    elif path == b'/comments':
        file = open('comment.html', 'rb')
        html = file.read()

        data = b'<p>'

        if os.path.exists('comment.txt'):
            file = open('comment.txt', 'rb')
            data += file.read()
            file.close()

        data = data.replace(b'\r\n\r\n', b'</p><p>')

        data += b'</p>'

        html = html.replace(b'{{comments}}', data)
        file.close()
        response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
        response += html
        request.sendall(response)

    elif path.startswith(b'/form-comment?'):
        path = path.replace(b'+', b' ')
        path = path.replace(b'%20', b' ')

        query = path.split(b'?')[1]
        query = query.split(b'&')

        name = query[0].split(b'=')[1]
        comment = query[1].split(b'=')[1]

        name = unquote_to_bytes(name)
        comment = unquote_to_bytes(comment)

        name = name.replace(b'<', b'&lt;')
        name = name.replace(b'>', b'&gt;')
        name = name.replace(b'&', b'&amp;')
        name = name.replace(b"'", b'&apos;')
        name = name.replace(b'"', b'&quot;')

        comment = comment.replace(b'<', b'&lt;')
        comment = comment.replace(b'>', b'&gt;')
        comment = comment.replace(b'&', b'&amp;')
        comment = comment.replace(b"'", b'&apos;')
        comment = comment.replace(b'"', b'&quot;')


        file = open('comment.txt', 'ab')
        file.write(name + b': ' + comment + b'\r\n\r\n')
        file.close()

        file = open('comment.html', 'rb')
        html = file.read()

        data = b'<p>'

        if os.path.exists('comment.txt'):
            file = open('comment.txt', 'rb')
            data += file.read()
            file.close()

        data = data.replace(b'\r\n\r\n', b'</p><p>')

        data += b'</p>'

        html = html.replace(b'{{comments}}', data)
        file.close()
        response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
        response += html
        request.sendall(response)

    elif path == b'/images':
        images_name = images_dict.keys()
        item1 = []
        item2 = []

        for name in images_name:
            item = b'<a href="/images/' + name + b'">' + name + b'</a><br>' + b'<a href="/images/' + name + b'"download>Download ' + name + b'</a><br>'
            item1.append(item)
            item = b'<img src="/images/' + name + b'">'
            item2.append(item)

        file = open('empty.html', 'rb')
        html = file.read()

        html = html.replace(b'{{title}}', b'images')
        html = html.replace(b'{{objects}}', b''.join(item1) + b''.join(item2))

        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/html\r\n'
        response += b'X-Content-Type-Options: nosniff\r\n'
        response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
        response += html
        request.sendall(response)

    elif path.startswith(b'/images/'):
        path = path.split(b'/images/')[1]

        image = b''

        if images_dict.get(path) is not None:
            image = images_dict[path]

        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: image/png\r\n'
        response += b'X-Content-Type-Options: nosniff\r\n'
        response += b'Content-Length: ' + str(len(image)).encode() + b'\r\n\r\n'
        response += image
        request.sendall(response)