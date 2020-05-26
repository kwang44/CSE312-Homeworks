import socketserver
import socket


# https://docs.python.org/3/library/socketserver.html

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        http_request = data = self.request.recv(4096).strip()
        data = data.split(b'\r\n')
        print(data)
        data = data[0].split(b' ')

        print(data)

        if data[0] == b'GET':
            if data[1] == b'/':
                response = b'HTTP/1.1 200 OK\r\n'
                response += b'Content-Type: text/plain\r\n'
                response += b'Content-Length: ' + str(len(http_request)).encode() + b'\r\n\r\n'
                response += http_request
                self.request.sendall(response)

            elif data[1] == b'/hello':
                message = b'Hello World!'
                response = b'HTTP/1.1 200 OK\r\n'
                response += b'Content-Type: text/plain\r\n'
                response += b'Content-Length: ' + str(len(message)).encode() + b'\r\n\r\n'
                response += message
                self.request.sendall(response)

            elif data[1] == b'/301':
                response = b'HTTP/1.1 301 Moved Permanently\r\n'
                response += b'Location: /hello\r\n'
                self.request.sendall(response)

            else:
                message = b'404 Page Not Found'
                response = b'HTTP/1.1 404 NOT FOUND\r\n'
                response += b'Content-Type: text/plain\r\n'
                response += b'Content-Length: ' + str(len(message)).encode() + b'\r\n\r\n'
                response += message
                self.request.sendall(response)

            self.request: socket.socket
            self.request.shutdown(socket.SHUT_RDWR)
            self.request.close()




        '''
        print(type(self.request))
        print("{} wrote:".format(self.client_address[0]))
        print(data.decode("utf-8"))
        self.request.sendall(data.upper())
        '''


if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()

