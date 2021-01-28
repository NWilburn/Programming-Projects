import socket, os, pickle, threading


def message_handler(conn_socket, server_directory):
    while True:
        service = conn_socket.recv(1024).decode("utf-8")
        if service.split("~~~")[0]=="send":
            send_message(service, server_directory, conn_socket)
        elif service.split("~~~")[0]=="check_for_user":
            check_for_user(service, server_directory, conn_socket)
        elif service.split("~~~")[0] == "get_message_history":
            get_message_history(service, server_directory, conn_socket)
        elif service.split("~~~")[0] == "login_user":
            login_user(service, server_directory, conn_socket)
        elif service == "close":
            conn_socket.close()
            break

def send_message(service, server_directory, conn_socket):
    if os.path.exists(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[1]}&{service.split('~~~')[2]}"):
        with open(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[1]}&{service.split('~~~')[2]}", "a") as f:
            f.write("\n" + service.split('~~~')[1] +":::{" + service.split('~~~')[4] + ",,[" + service.split('~~~')[3])
    else:
        with open(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[2]}&{service.split('~~~')[1]}", "a") as f:
            f.write("\n" + service.split('~~~')[1] + ":::{" + service.split('~~~')[4] + ",,[" + service.split('~~~')[3])
    conn_socket.send(("Delivered").encode("utf-8"))


def check_for_user(service, server_directory, conn_socket):
    if os.path.exists(f"{server_directory}\\User Directory\\{service.split('~~~')[1]}"):
        conn_socket.send(("User exists").encode("utf-8"))
    else:
        conn_socket.send(("User does not exist").encode("utf-8"))


def get_message_history(service, server_directory, conn_socket):
    if os.path.exists(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[1]}&{service.split('~~~')[2]}"):
        with open(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[1]}&{service.split('~~~')[2]}", "r") as f:
            conn_socket.send(pickle.dumps(f.readlines()))
    elif os.path.exists(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[2]}&{service.split('~~~')[1]}"):
        with open(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[2]}&{service.split('~~~')[1]}", "r") as f:
            conn_socket.send(pickle.dumps(f.readlines()))
    else:
        with open(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[1]}&{service.split('~~~')[2]}", "w") as f:
            f.write("")
        with open(f"{server_directory}\\Conversation Directory\\{service.split('~~~')[1]}&{service.split('~~~')[2]}", "r") as f:
            conn_socket.send(pickle.dumps(f.readlines()))


def login_user(service, server_directory, conn_socket):
    if os.path.exists(f"{server_directory}\\User Directory\\{service.split('~~~')[1]}"):
        with open(f"{server_directory}\\User Directory\\{service.split('~~~')[1]}\\password.txt", "r") as f:
            if f.read() == service.split("~~~")[2]:
                conn_socket.send(("True").encode("utf-8"))
            else:
                conn_socket.send(("Incorrect Password.").encode("utf-8"))
    else:
        conn_socket.send(("User does not exist.").encode("utf-8"))

if __name__ == '__main__':
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('10.0.0.34', 59634))
    serverSocket.listen(5)
    sDirectory = os.path.dirname(__file__)
    print("Server is ready to go")
    while True:
        connSocket, addr = serverSocket.accept()
        print(f"Connection established from {addr}")
        threading.Thread(target=message_handler, args=(connSocket, sDirectory)).start()