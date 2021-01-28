import socket,time,os


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

uri = input("Input target uri: ")

try:
    clientSocket.connect(('192.168.0.26', 9876))
    clientSocket.send(("GET /" + uri.split('/')[1]).encode("utf-8"))
    msg_complete = False
    html_page = ''
    header_OK = 'HTTP/1.1 200 OK\r\n\r\n'
    header_ERROR = 'HTTP/1.1 404 ERROR\r\n\r\n'
    while msg_complete == False:
        html_data = clientSocket.recv(1024)
        new_data = html_data.decode("utf-8")
        if html_data == b'':
            msg_complete = True
        if new_data != header_OK and new_data != header_ERROR and new_data != b'':
            html_page += new_data
    f = open('.html', 'w')
    f.write(html_page)
    f.close()
    os.startfile('test.html')
except ConnectionRefusedError:
    print("Could not establish connection")

time.sleep(10)