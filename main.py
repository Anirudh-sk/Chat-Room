import threading 
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
nicknames=[]

def brodcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message= client.recv(1024)
            brodcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            brodcast(f'{nickname} left the room !'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'connected {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'{nickname} is joined')
        brodcast(f'{nickname} joined the room'.encode('ascii'))
        client.send('connected to setvet !'.encode('ascii'))

        thread= threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server running ........')
receive()