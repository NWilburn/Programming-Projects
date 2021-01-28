import socket, os, codecs

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('0.0.0.0', 9876))
serverSocket.listen(5)
server_directory = os.path.dirname(__file__)
print("Server is ready to go\n")
while True:
    connSocket, addr = serverSocket.accept()
    connSocket.settimeout(10)
    print(f"Connection established from {addr}")
    try:
        http_message = connSocket.recv(1024)
        print(http_message.decode("utf-8"))
        input_name = http_message.decode("utf-8").split()[1]
        html_file = codecs.open(server_directory + input_name, "r")
        output_page = html_file.read()
        connSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8'))
        for i in range(0, len(output_page)):
            connSocket.send(output_page[i].encode('utf-8'))
        print("Client sent to page\n")
        connSocket.close()
    except IOError:
        connSocket.send('HTTP/1.1 404 ERROR\r\n\r\n'.encode("utf-8"))
        connSocket.send("404 Error".encode("utf-8"))
        print("Error\n")
        connSocket.close()
serverSocket.close()