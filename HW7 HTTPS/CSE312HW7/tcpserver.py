import socketserver
import socket
import hashlib
import base64
import json
import ssl

# https://docs.python.org/3/library/socketserver.html

socket_set = set()


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # print(type(self.request))
        http_request = data = self.request.recv(4096).strip()

        self.request: socket.socket

        print(data)

        if not data:
            return

        post_data = None
        print("---------------------************************************************************************************************------------------------------")
        data: bytes

        data_list = data.split(b'\r\n')
        # print(data_list)
        pathing = data_list[0].split(b' ')
        # print(pathing)

        derp = {}
        for item in data_list:
            temp = item.split(b' ', 1)
            derp[temp[0]] = temp[1]

        if pathing[0] == b'GET':
            path = pathing[1]
            # print(path)
            if path == b'/':
                file = open('index.html', 'rb')
                html = file.read()
                file.close()
                response = b'HTTP/1.1 200 OK\r\n'
                response += b'Content-Type: text/html\r\n'
                response += b'X-Content-Type-Options: nosniff\r\n'
                response += b'Content-Length: ' + str(len(html)).encode() + b'\r\n\r\n'
                response += html
                self.request.sendall(response)

            elif path == b'/index.js':
                file = open('index.js', 'rb')
                js = file.read()
                file.close()
                response = b'HTTP/1.1 200 OK\r\n'
                response += b'Content-Type: text/javascript\r\n'
                response += b'X-Content-Type-Options: nosniff\r\n'
                response += b'Content-Length: ' + str(len(js)).encode() + b'\r\n\r\n'
                response += js
                self.request.sendall(response)

            elif path == b'/htmlmeme.png':
                file = open('htmlmeme.png', 'rb')
                img = file.read()
                file.close()

                response = b'HTTP/1.1 200 OK\r\n'
                response += b'Content-Type: image/jpeg\r\n'
                response += b'X-Content-Type-Options: nosniff\r\n'
                response += b'Content-Length: ' + str(len(img)).encode() + b'\r\n\r\n'
                response += img
                self.request.sendall(response)

            elif path == b'/socket':
                key = derp[b'Sec-WebSocket-Key:']
                # print(key)
                key += '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'.encode()
                hash_string = base64.b64encode(hashlib.sha1(key).digest())
                # print(hash_string)

                response = b'HTTP/1.1 101 Switching Protocols\r\n'
                response += b'Upgrade: websocket\r\n'
                response += b'Connection: Upgrade\r\n'
                response += b'Sec-WebSocket-Accept: ' + hash_string + b'\r\n\r\n'
                self.request.sendall(response)

                socket_set.add(self.request)

                while data:
                    try:
                        data = self.request.recv(4096)
                    except:
                        break

                    if not data:
                        break

                    if data and data[0] == 0b10000001:
                        payload = b''
                        bit_mask = b''
                        payload = b''
                        payload_len = data[1] & 0b01111111

                        if payload_len == 126:
                            payload_len = int.from_bytes(data[2:4], byteorder='big', signed=False)
                            print("Payload length: " + str(payload_len))
                            bit_mask = data[4:8]
                            payload = data[8: 8 + payload_len]
                        elif payload_len == 127:
                            payload_len = int.from_bytes(data[2:10], byteorder='big', signed=False)
                            print("Payload length: " + str(payload_len))
                            bit_mask = data[10:14]
                            payload = data[14: 14 + payload_len]
                        else:
                            print("Payload length: " + str(payload_len))
                            bit_mask = data[2:6]
                            payload = data[6: 6 + payload_len]

                        string_data = bytearray(payload_len)

                        for i, chunk in enumerate(payload):
                            string_data[i] = chunk ^ bit_mask[i % 4]

                        print(string_data)
                        json_dict = json.loads(string_data)
                        print(json_dict)

                        response = bytearray()
                        response.append(0b10000001)
                        # print(payload_len.to_bytes(8, byteorder='big', signed=False))

                        if payload_len >= 65536:
                            response.append(0b01111111)
                            response += payload_len.to_bytes(8, byteorder='big', signed=False)
                        elif payload_len >= 126:
                            response.append(0b01111110)
                            response += payload_len.to_bytes(2, byteorder='big', signed=False)
                        else:
                            response += payload_len.to_bytes(1, byteorder='big', signed=False)

                        response += string_data

                    for sock in socket_set:
                        try:
                            sock.sendall(response)
                        except:
                            continue;

                socket_set.discard(self.request)
                print("Socket ended")


if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    '''''with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()'''''

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.socket = ssl.wrap_socket(server.socket, keyfile='./private.key', certfile='./cert.pem', server_side=True)
        server.serve_forever()
