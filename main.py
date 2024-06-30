import socket
import threading
import rsa
import sys


def clear_last_line():
    # Move the cursor up one line
    sys.stdout.write('\x1b[1A')
    # Clear the line
    sys.stdout.write('\x1b[2K')




public_key, private_key= rsa.newkeys(1024)
public_key_parter = None

choice = input('''What you want to connect to 
    press 1. Host
    press 2. Client
''')

if choice =='1':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind( (socket.gethostbyname(socket.gethostname()) , 8080) )
    server.listen(1)
    client, _ = server.accept()
    client.send( public_key.save_pkcs1("PEM"))
    public_key_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    

elif choice=='2':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect (( socket.gethostbyname(socket.gethostname()), 8080))
    public_key_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send( public_key.save_pkcs1("PEM"))


else : 
    exit()

def sending_messages (client) :
    while True:
        message = input("")
        clear_last_line()

        client.send(rsa.encrypt(message.encode(),public_key_partner))
        print("YOU: "+message)


def receiving_messages (client):
    while True:
        print("Partner: "+ rsa.decrypt(client.recv(1024), private_key).decode())

threading.Thread(target= sending_messages, args=(client,)).start()
threading.Thread(target= receiving_messages, args= (client,)).start()