import socketserver
import getrequest
import postrequest

# https://docs.python.org/3/library/socketserver.html

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        #print(type(self.request))
        http_request = data = self.request.recv(4096).strip()

        if not data:
            return

        post_data = None

        print(data)
        print("---------------------************************------------------------------")

        if b'\r\n\r\n' in data:
            data = data.split(b'\r\n\r\n', 1)
            post_data = data[1]
            data = data[0]

        data = data.split(b'\r\n')
        http_request: bytes
        http_request_dict = {}

        for data_string in data:
            data_string = data_string.split(b' ', 1)
            data_string: list
            http_request_dict[data_string[0]] = data_string[1]

        if http_request_dict.get(b'GET') is not None:
            getrequest.get_request(http_request_dict, self.request)
        elif http_request_dict.get(b'POST') is not None:
            postrequest.post_request(http_request_dict, self.request, post_data)



if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    '''''with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()'''''

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
