import tcpserver
import socketserver
import socket
import tcpserver
import getrequest


def post_request(data: dict, request: socket.socket, post_data: bytes = None):
    path = data[b'POST'].split(b' ', 1)[0]
    print(post_data)

    if path == b'/form-upload':

        boundary = data[b'Content-Type:'].split(b'boundary=')[1]
        boundary = b'\r\n--' + boundary + b'--'
        print(boundary)

        image_data = []
        if post_data is not None:
            image_data.append(post_data)

        while len(image_data) == 0 or boundary not in image_data[-1]:
            temp_data = request.recv(4096)
            if not temp_data:
                break
            image_data.append(temp_data)


        image_data = b''.join(image_data)
        data_index_front = image_data.index(b'\r\n\r\n') + len(b'\r\n\r\n')
        data_index_back = image_data.rindex(boundary)
        image_data = image_data[data_index_front: data_index_back]

        file_name = b'image' + str(len(getrequest.images_dict) + 1).encode() + b'.png'
        getrequest.images_dict[file_name] = image_data

        file = open('empty.html', 'rb')
        html = file.read()

        html = html.replace(b'{{title}}', b'Submitted')
        html = html.replace(b'{{objects}}', b'Your file has been submitted')

        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/html\r\n'
        response += b'X-Content-Type-Options: nosniff\r\n'
        response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
        response += html
        request.sendall(response)


