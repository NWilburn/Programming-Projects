import socket, time, datetime, pickle, threading

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_message(user):
    target = input("Who would you like to chat with?: ")
    check_user_exist(target)
    threading.Thread(target=check_for_updates, args=(user,target)).start()
    while True:
        message = input("Enter message: ")
        if message == "LEAVE":
            break
        else:
            timestamp = str(datetime.datetime.now())
            clientSocket.send(("send~~~" + user.strip() + "~~~" + target.strip() + "~~~" + timestamp + "~~~" + message).encode("utf-8"))
            outcome = clientSocket.recv(1024).decode("utf-8")
            print(outcome)


def check_user_exist(user):
    clientSocket.send(("check_for_user~~~" + user).encode("utf-8"))
    user_exist = clientSocket.recv(1024).decode("utf-8")
    if user_exist == "User does not exist":
        new_user = input("User does not exist. Enter username that exists: ")
        check_user_exist(new_user)


def get_message_history(user, target, most_recent_message):
    clientSocket.send(("get_message_history~~~" + user.strip() + "~~~" + target.strip()).encode("utf-8"))
    data = []
    while True:
        packet = clientSocket.recv(1024)
        data.append(packet)
        if len(packet) < 1024:
            break
    message_history = pickle.loads(b"".join(data))
    if most_recent_message != message_history[len(message_history) - 1]:
        for p in message_history:
            if p != "\n":
                print(f"{p.split(':::{')[0]}: {p.split(':::{')[1].split(',,[')[0]}")
        timestamps = []
        for q in message_history:
            if q != "\n":
                timestamps.append(p.split(':::{')[1].split(',,[')[1])
        return message_history[len(message_history) - 1]
    else:
        return most_recent_message


def check_for_updates(user, target):
    most_recent_message = ""
    while True:
        most_recent_message = get_message_history(user, target, most_recent_message)
        time.sleep(5)


def login_user(user, password):
    clientSocket.send(("login_user~~~" + user.strip() + "~~~" + password.strip()).encode("utf-8"))
    return clientSocket.recv(1024).decode("utf-8")


if __name__ == '__main__':
    try:
        clientSocket.connect(('10.0.0.34', 59634))    
        print("Welcome to pyMessenger")
        user_logged_in = False
        while user_logged_in != True:
            user = input("Enter username: ")
            password = input("Enter password: ")
            user_logged_in = login_user(user, password)

            if user_logged_in == "True":
                user_logged_in = True
            else:
                print(user_logged_in)
                
        while True:
            cmd = input("Would you like to send a message? ")
            if cmd == "yes":
                send_message(user)
            else:
                clientSocket.send(("close").encode("utf-8"))
                clientSocket.close()
                break
    except ConnectionRefusedError:
        print("Could not establish connection")