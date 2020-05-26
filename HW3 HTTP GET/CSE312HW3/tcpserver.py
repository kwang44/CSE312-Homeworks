import socketserver

# https://docs.python.org/3/library/socketserver.html

globals_dict = {}
comments = []


class MyTCPHandler(socketserver.BaseRequestHandler):

    def myGET(self, path, cookie=None):

        path: bytes
        cookie: bytes

        if path == b'/' or path == b'/table.html':

            my_html = globals_dict['table.html']

            new_cookie = b''

            if cookie is not None:
                visit_cookie_value = None
                list = cookie.split(b'; ')
                for li in list:
                    if li.startswith(b'visits='):
                        visit_cookie_value = li.split(b'=')[1]
                if visit_cookie_value is not None and visit_cookie_value.isdigit():
                    cookie = int(visit_cookie_value)
                    cookie += 1
                    new_cookie = str(cookie).encode()
                    my_html = my_html[0] + b'<h1>Cookie say this is your ' + new_cookie + b' visits, (Cookie Max-Age is ' \
                                                                                          b'set to 10 seconds so it will ' \
                                                                                          b'reset after 10 seconds of not ' \
                                                                                          b'visiting this page)</h1> <img ' \
                                                                                          b'src="cookiememes.jpg" ' \
                                                                                          b'alt="random meme">' + my_html[1]
                    new_cookie = b'visits=' + new_cookie
            if not new_cookie:
                my_html = my_html[0] + b'<h1>No visits cookies has been set (Cookie Max-Age is set to 10 seconds so it ' \
                                       b'will reset after 10 seconds of not visiting this page)</h1>' + my_html[1]
                new_cookie = b'visits=1'

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: text/html\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Set-Cookie: ' + new_cookie + b'; Max-Age=10\r\n'
            response += b'Content-Length: ' + str(len(my_html)).encode() + b'\r\n\r\n'
            response += my_html
            self.request.sendall(response)

        elif path == b'/list.html':

            my_html = globals_dict['list.html']

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: text/html\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(my_html)).encode() + b'\r\n\r\n'
            response += my_html
            self.request.sendall(response)

        elif path == b'/style.css':

            my_html = globals_dict['style.css']

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: text/css\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(my_html)).encode() + b'\r\n\r\n'
            response += my_html
            self.request.sendall(response)

        elif path == b'/script.js':

            my_html = globals_dict['script.js']

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: text/javascript\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(my_html)).encode() + b'\r\n\r\n'
            response += my_html
            self.request.sendall(response)

        elif path == b'/randomimage.jpg':

            my_html = globals_dict['randomimage.jpg']

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: image/jpeg\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(my_html)).encode() + b'\r\n\r\n'
            response += my_html
            self.request.sendall(response)

        elif path == b'/cookiememes.jpg':

            my_html = globals_dict['cookiememes.jpg']

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: image/jpeg\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(my_html)).encode() + b'\r\n\r\n'
            response += my_html
            self.request.sendall(response)

        elif path == b'/comments':

            message = b'Use ?add=<message> to add a comment and ?remove=<index> to remove a comment(index start at ' \
                      b'0)\r\nUse \'+\' or %20 as space\r\n\r\nThe Comments in list:\r\n\r\n\r\n'

            for i, b in enumerate(comments):
                message += str(i).encode() + b': ' + b + b'\r\n\r\n'

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: text/plain\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(message)).encode() + b'\r\n\r\n'
            response += message
            self.request.sendall(response)

        elif path.startswith(b'/comments?add='):

            text = path.split(b'=', 1)[1]

            if text:
                text = text.replace(b'+', b' ')
                text = text.replace(b'%20', b' ')
                comments.append(text)

            message = b'Use ?add=<message> to add a comment and ?remove=<index> to remove a comment(index start at ' \
                      b'0)\r\nUse \'+\' or %20 as space\r\n\r\nThe Comments in list:\r\n\r\n\r\n'

            for i, b in enumerate(comments):
                message += str(i).encode() + b': ' + b + b'\r\n\r\n'

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: text/plain\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(message)).encode() + b'\r\n\r\n'
            response += message
            self.request.sendall(response)

        elif path.startswith(b'/comments?remove='):
            index = path.split(b'=', 1)[1]

            if index.isdigit():
                index = int(index)
                if index >= 0 and index < len(comments):
                    comments.pop(index)

            message = b'Use ?add=<message> to add a comment and ?remove=<index> to remove a comment(index start at ' \
                      b'0)\r\nUse \'+\' or %20 as space\r\n\r\nThe Comments in list:\r\n\r\n\r\n'

            for i, b in enumerate(comments):
                message += str(i).encode() + b': ' + b + b'\r\n\r\n'

            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: text/plain\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(message)).encode() + b'\r\n\r\n'
            response += message
            self.request.sendall(response)

        elif path == b'/301':
            response = b'HTTP/1.1 301 Moved Permanently\r\n'
            response += b'Location: /\r\n'
            self.request.sendall(response)

        else:
            message = b'404 Page Not Found'
            response = b'HTTP/1.1 404 NOT FOUND\r\n'
            response += b'Content-Type: text/plain\r\n'
            response += b'X-Content-Type-Options: nosniff\r\n'
            response += b'Content-Length: ' + str(len(message)).encode() + b'\r\n\r\n'
            response += message
            self.request.sendall(response)

    def handle(self):
        http_request = data = self.request.recv(4096).strip()

        if not data:
            return

        data = data.split(b'\r\n')
        http_request: bytes

        http_request_dict = {}

        for data_string in data:
            data_string = data_string.split(b' ', 1)
            data_string: list
            http_request_dict[data_string[0]] = data_string[1]

        if http_request_dict.get(b'GET') is not None:
            self.myGET(http_request_dict.get(b'GET').split(b' ')[0], http_request_dict.get(b'Cookie:'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    file = open('table.html', 'rb')
    globals_dict['table.html'] = file.read()
    file.close()

    globals_dict['table.html'] = globals_dict['table.html'].split(b'<div id="thisDivTagHasNoPurpose"></div>')

    file = open('list.html', 'rb')
    globals_dict['list.html'] = file.read()
    file.close()

    file = open('style.css', 'rb')
    globals_dict['style.css'] = file.read()
    file.close()

    file = open('script.js', 'rb')
    globals_dict['script.js'] = file.read()
    file.close()

    file = open('randomimage.jpg', 'rb')
    globals_dict['randomimage.jpg'] = file.read()
    file.close()

    file = open('cookiememes.jpg', 'rb')
    globals_dict['cookiememes.jpg'] = file.read()
    file.close()

    '''''with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()'''''

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
